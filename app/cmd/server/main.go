package main

import (
	"fmt"
	"io"
	"io/fs"
	"log"
	"mime"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	app "github.com/austindoeswork/sfbay.dance/app"
)

func main() {
	// config
	c, err := app.GetConfig()
	if err != nil {
		log.Println("Error while loading config")
		log.Println(err)
	}

	mux := http.NewServeMux()

	// handlers

	// path: /
	if c.Env == "prod" || c.Env == "test" {
		// runs from embedded in prod
		mux.HandleFunc("/", handleSite)
	} else {
		// runs "raw" in dev mode
		devHandler := http.StripPrefix("/", http.FileServer(http.Dir("./_ui/build")))
		mux.Handle("/", devHandler)
	}

	// path: /assets/
	assetHandler := http.StripPrefix("/assets/", http.FileServer(http.Dir("./assets")))
	mux.Handle("/assets/", assetHandler)

	var httpErr error
	if c.Env == "prod" {
		go http.ListenAndServe(":80", http.HandlerFunc(redirect))

		certFile := c.CertFile
		keyFile := c.KeyFile
		log.Printf("\nRUNNING IN: PRODUCTION...\n")
		httpErr = http.ListenAndServeTLS(c.Port, certFile, keyFile, mux)
	} else {
		log.Printf("\nRUNNING IN: DEVELOPMENT...\n")
		httpErr = http.ListenAndServe(c.Port, mux)
	}
	if httpErr != nil {
		log.Println("server failed:", httpErr)
	}

}

func handleSite(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	path := filepath.Clean(r.URL.Path)
	if path == "/" { // Add other paths that you route on the UI-side here
		path = "index.html"
	}
	path = strings.TrimPrefix(path, "/")

	file, err := uiFS.Open(path)
	if err != nil {
		if os.IsNotExist(err) {
			log.Println("file", path, "not found:", err)
			http.NotFound(w, r)
			return
		}
		log.Println("file", path, "cannot be read:", err)
		http.Error(w, http.StatusText(http.StatusInternalServerError), http.StatusInternalServerError)
		return
	}

	contentType := mime.TypeByExtension(filepath.Ext(path))
	w.Header().Set("Content-Type", contentType)
	if strings.HasPrefix(path, "static/") {
		w.Header().Set("Cache-Control", "public, max-age=31536000")
	}
	stat, err := file.Stat()
	if err == nil && stat.Size() > 0 {
		w.Header().Set("Content-Length", fmt.Sprintf("%d", stat.Size()))
	}

	n, _ := io.Copy(w, file)

	// TODO better logging
	log.Println("file", path, "copied", n, "bytes")
}

func redirect(w http.ResponseWriter, req *http.Request) {
	http.Redirect(w, req,
		"https://"+req.Host+req.URL.String(),
		http.StatusMovedPermanently)
}

var uiFS fs.FS

func init() {
	var err error
	uiFS, err = fs.Sub(app.UI, "_ui/build")
	if err != nil {
		log.Fatal("failed to get ui fs", err)
	}
}

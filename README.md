# SFBAY.DANCE

## SUMMARY

sfbay.dance is a dance class aggregator for the San Francisco Bay Area. It has been built by dancers, for dancers.

We are not affiliated with any studio.

The structure of this application is rather bare bones:

- `scraper/` contains:
	- the python code for scraping dance sites
	- the "database" code for generating a json file containing all of the dance events
- `app/`:
	- `cmd/src/` contains:
		- the go server code for hosting the frontend and dance event json as a static file
	- `_ui/` contains: 
		- the React frontend code

Notes:

- The server and frontend are built and hosted as a single binary file
- The scraper will run periodically as a cron job

## Cloning

```
# clone repo
% git clone git@github.com:austindoeswork/sfbay.dance.git
% cd sfbay.dance
```


## SERVER dev setup

```
# install golang
% brew install go


```
## SCRAPER dev setup

```
# check python version
% python3 --version
Python 3.10.6


# setup python env
% python3 -m venv venv
% source venv/bin/activate
% pip install -r requirements.txt
% pip install -e .

# create a config in scrape/scraper_config.json
{
	"db_path": "/<PATH_TO>/sfbay.dance/app/assets/events.json"
}
# create the events json file
% echo "{}" > /<PATH_TO>/sfbay.dance/app/assets/events.json

# to run the scraper
% python collect.py
```

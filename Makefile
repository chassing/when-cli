all: download process

download:
	@mkdir -p dump
	@curl --progress-bar -L http://download.geonames.org/export/dump/cities15000.zip > dump/cities15000.zip
	@cd dump; unzip -o cities15000.zip; rm -f cities15000.zip

process:
	@python generate_cities.py

.PHONY: all download process

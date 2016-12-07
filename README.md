# eBird Digest

Creates a daily digest, of recent sightings of target bird species in given regions, using the eBird API.

The [eBird Needs Alert](http://ebird.org/ebird/alerts) performs this same function, but the needs and search scope must be on the same geographic scale. For instance, it generates a list of Massachusetts needs, and returns sightings of those birds in Massachusetts.

While undoubtedly useful, there are many areas where customization might be preferable. For instance:
* Continent-level needs, across surrounding states
* State-level needs, but only within certain counties
* Excluding certain needs (eBird's Needs Alerts can be a fire hose when first visiting an area)
* Including species that aren't needs, but where additional observations would be good to follow up on.

The eBird Digest allows for a more personalized digest of relevant information.

## Current progress

* User manually creates a list of targets in `targets.csv`
* The `eBirdDigest.py` script finds sightings of those targets in the past day
* The script then lists those sightings in an HTML file, `todaysdigest.html`
    * If the location is a hotspot, a link to the hotspot's eBird page is provided. If not, a link to Apple Maps is provided (Google Maps implementation is in the code as well, commented out)

## To do

* Schedule the script to run at certain times each day, for instance generating a fresh new digest each morning
* Two options for digest presentation:
    * Send an email to the user
    * Host a website that refreshes each day (and on-demand as well?)
* Could optionally attach notable bird sightings as well (ex: state-level Rare Bird Alerts)

## Issues

* Unfortunately, the eBird API doesn't return information the checklists providing these sightings.
    * So no web links to the specific checklists are possible
    * Also, any observer comments, photos, etc. are also not linkable
    * Observer name is also not available, which could've provided some first-pass vetting
    * There could be other paths to getting this information, but it would likely have to involve web scraping outside of the official eBird API


## Footnotes
* Roger Shaw
* Currently a fellow at Insight Health Data Science, transitioning from academia into a career in data science
* As can be inferred from this project's goals, I'm an avid birder in my spare time, and so this project was borne out of my own need for this tool!
* [Python eBird API Wrapper gratiously forked from Carson McDonald](https://github.com/carsonmcdonald/python-ebird-wrapper)

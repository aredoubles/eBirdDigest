from ebird import AvianKnowledge
from ebird import EBird
import pandas as pd
import pypandoc

ak = AvianKnowledge()
ebird = EBird()

# print ebird.recent_species_observations_region('subnational1', 'US-KY',
# 'Hirundo rustica')

'''
What's the plan?
- Go through each line of csv
- Lookup in eBird API
    - Change recency to 1 day
- If present, save in DataFrame
- Parse dataframe, print
'''


def eBirdLookup(targets):
    # Import Clements/eBird checklist
    specieslist = pd.read_csv(
        'eBird_Taxonomy_v2016_9Aug2016.csv', engine='python')
    specieslist = specieslist.set_index('PRIMARY_COM_NAME')

    todaysum = pd.DataFrame()

    for index, species, scale, region in targets.itertuples():

        # Look up scientific name of each species
        sciname = specieslist.ix[species]['SCI_NAME']

        '''
        What to do about counties? Would have to be encoded 'US-TX-009' or something?
        Is there a way to look it up with the Avian Knowledge API?
        '''

        # Look up each species/region in EBird
        # If present, save in dataframe `todaysum`
        if scale == 'State':
            level = 'subnational1'
            region = 'US-' + region
        elif scale == 'County':
            level = 'subnational2'

        recs1 = ebird.recent_species_observations_region(
            level, region, sciname)
        # Seems to be ignoring the 'back' part of the API lookup, looks back ~2 weeks
        # So manually draw out the date, and exlude all but yesterday's?

        sppdf = pd.DataFrame(recs1)
        sppdf['Region'] = region

        if todaysum.empty:
            todaysum = sppdf
        else:
            todaysum = pd.concat([todaysum, sppdf])

    return todaysum


def ParsePrint(todaysum):
    # Take the 'todaysum' dataframe, and create a markdown file 'newdoc' with
    # relevant information, even including links to checklists and locations
    newdoc = open('todaysdigest.md', 'w')

    newdoc.write(r'## Sightings of your target species in the past day:')
    newdoc.write('\n \n')

    # Surely there's a more concise way to code this...
    for index, record in todaysum.iterrows():
        # If location is an eBird hotspot, link to that page. Else, link to Google/Apple Maps
        if record['locationPrivate'] == False:
            maplink = '{}{}{}{}'.format('(', 'http://ebird.org/ebird/hotspot/', record['locID'], ')')
        else:
            # Currently I prefer Apple Maps, so here's the URL for that
            maplink = '{}{}{}{}{}{}'.format('(', 'http://maps.apple.com/?q=', record['lat'], ',', record['lng'], ')')

            # URL of location on Google Maps
            '''maplink = '{}{}{}{}{}{}{}{}{}{}'.format('(', 'http://maps.google.com/?ie=UTF8&t=p&z=13&q=',
                                                record['lat'], ',', record['lng'], '&ll=',
                                                record['lat'], ',', record['lng'], ')'
                                                )'''

        # Name of location within Markdown's square brackets
        mdloc = '{}{}{}'.format('[', record['locName'], ']')

        newdoc.write(r'###')
        newdoc.write(record['comName'])
        newdoc.write(' (')
        newdoc.write(str(int(record['howMany'])))
        newdoc.write(')')
        newdoc.write('\n \n')
        newdoc.write(str(record['obsDt']))
        newdoc.write('\n \n')
        newdoc.write(mdloc)
        newdoc.write(maplink)
        newdoc.write('\n \n')
        newdoc.write(record['Region'])
        newdoc.write('\n \n')
        newdoc.write('\n \n')

    newdoc.close()

    # Conver this markdown file to HTML
    output = pypandoc.convert_file('todaysdigest.md', 'html')

    thesite = open('todaysdigest.html', 'w')
    thesite.write(output)
    thesite.close()

    return newdoc    # Or could return the HTML file, depends on what emailing wants

    '''
    How might I get links to the locations, or to the checklists involved?
    The checklist information is NOT included in these API returns, which is very unfortunate.
    Any way to use the observation date and location to find them elsewhere in the API?

    '''


def EmailDigest(newdoc):
    # Email the 'newdoc' text file to my address
    cray = 2


def main():
    targets = pd.read_csv('targets.csv')
    todaysum = eBirdLookup(targets)
    newdoc = ParsePrint(todaysum)
    # EmailDigest(newdoc)
    #todaysum.to_csv('todaysum.csv')

main()


'''
Actual alert entry from eBird, to model after:

Rufous Hummingbird (Selasphorus rufus) (3) CONFIRMED
- Reported Aug 16, 2016 18:12 by Andy & Ellen Filtness
- Brittlyns Ct., Travis, Texas
- Map: http://maps.google.com/?ie=UTF8&t=p&z=13&q=30.3834554,-97.8517178&ll=30.3834554,-97.8517178
- Checklist: http://ebird.org/ebird/view/checklist/S31124374
- Media: 4 Photos
- Comments: "Continuing adult male & immature male & adult female (?)"
'''

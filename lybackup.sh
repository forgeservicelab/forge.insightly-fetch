#!/bin/bash

# Have your Insightly key stored in the INSIGHTLY_KEY environment variable before running this.

./lyfetch.py -c > lyconctacs.json
./lyfetch.py -o > lyorganisations.json
./lyfetch.py -p > lyprojects.json
./lyfetch.py -g > lyprojectcategories.json
./lyfetch.py -r > lyopportunities.json
./lyfetch.py -t > lyopportunitycategories.json
./lyfetch.py -i > lypipelines.json
./lyfetch.py -s > lypipelinestages.json
./lyfetch.py -u > lyopportunitystatereasons.json

filename="lybackup-$(date '+%Y-%m-%dT%H.%M.tgz')"
tar cvzf $filename ly*.json

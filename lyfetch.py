#!/usr/bin/python

# lyfetch.py
# Copyright (c) 2015 DIGILE Ltd
# License: MIT
# Author: Pasi Kivikangas

"""
Fetches data from Insightly in json format. Provide your insightly key as
a parameter or have it stored in INSIGHTLY_KEY environment variable.

Usage: 
  lyfetch.py [-hcopgrtisua] [INSIGHTLY_KEY]

Options: 
  -h  help.
  -c  fetch contacts.
  -o  fetch organisations.
  -p  fetch projects.
  -g  fetch project categories.
  -r  fetch opportunities.
  -t  fetch opportunity categories.
  -i  fetch pipelines.
  -s  fetch pipeline stages.
  -u  fetch opportunity reasons.
  -a  fetch and archive all into a tar file instead of stdout.

"""

from docopt import docopt
from os import getenv
import sys
import getopt
import requests
import tarfile
import time
import json

def fetch(url, key):
    if url and key is not "":
        r = requests.get(url, auth=(key, ''))
        if r.status_code == 200:
            return r.json()
        else:
            print "Error %s: Either the Insightly key is incorrect or API has changed" % (r.status_code)
            return False


def get_from_env_or_prompt(varname, echo=True):
    """Get an environment variable, if it exists, or query the user for it"""
    value = getenv(varname)
    if value is None or value is "":
        print '%s not found in env.' % varname
        if echo:
            value = raw_input('Have your Insightly API key stored in INSIGHTLY_KEY environment variable or enter the value: ')
        else:
            value = getpass('Have your Insightly API key stored in INSIGHTLY_KEY environment variable or enter the value: ')
    return value

def main(arg):
    api = {}
    api['-c'] = "https://api.insight.ly/v2.1/Contacts"
    api['-o'] = "https://api.insight.ly/v2.1/Organisations"
    api['-p'] = "https://api.insight.ly/v2.1/Projects"
    api['-g'] = "https://api.insight.ly/v2.1/ProjectCategories"
    api['-r'] = "https://api.insight.ly/v2.1/Opportunities"
    api['-t'] = "https://api.insight.ly/v2.1/OpportunityCategories"
    api['-i'] = "https://api.insight.ly/v2.1/Pipelines"
    api['-s'] = "https://api.insight.ly/v2.1/PipelineStages"
    api['-u'] = "https://api.insight.ly/v2.1/OpportunityStateReasons"
    url = None
    archive = False

    key = arg['INSIGHTLY_KEY'] or get_from_env_or_prompt("INSIGHTLY_KEY")  
    if not key:
        print "Error: Insightly key was not provided"
        sys.exit(1)
    
    # def writeToFile(url):
    #     fname = url.split('/')[-1] + '.json'
    #     f = open(fname, 'w')
    #     f.write(fetch(url, key))
    #     f.close()
    #     return fname

    if arg['-a']:
        today = time.strftime("%Y-%m-%dT%H:%M")
        archfile = tarfile.open("insightlybackup_%s.tar.gz" % (today), "w|gz")
        # map(archfile.add, map(writeToFile, api.items()))
        for k,v in api.items():
            url = v
            data = fetch(url, key)
            fname = url.split("/")
            fname = fname[4] + ".json"
            f = open(fname, "w")
            f.write(json.dumps(data))
            f.close()
            archfile.add(fname, fname)
        archfile.close()
    else:
        #print map(lambda data: fetch(api[data], key), filter(lambda k: k in api.keys(), arg.keys()))
        for k,v in arg.items():
            for kk,vv in api.items():
                if k==kk and v: # a given argument was found and matches api too
                    data = fetch(vv, key)
                    if data:
                        print data
                    else:
                        exit(1)

if __name__ == "__main__":
    arg = docopt(__doc__)
    main(arg)


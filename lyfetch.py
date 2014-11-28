#!/usr/bin/python

# Fetches bulk data from Insightly with provide API key
#
# Copyright 2014 DIGILE Ltd
# Author: Pasi Kivikangas
# License: TBD

from os import getenv
import sys
import getopt
import requests
import tarfile
import time

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


def help():
    print """
    Fetches data from Insightly in json format. Provide your insightly key as
    a parameter or have it stored in INSIGHTLY_KEY environment variable.

    Usage: lyfetch.py [-k <insightly_key>] [-c] [-o] [-p] [-g] [-r] [-t] [-i] [-s] [-u] [-a]

           -k <insightly_key>
           -c contacts
           -o organisations
           -p projects
           -g project categories
           -r opportunities
           -t opportunity categories
           -i pipelines
           -s pipeline stages
           -u opportunity reasons
           -a archive everything at once 

           -h help
    """


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:coapgrtisua")
    except getopt.GEtoptError:
        help()
        sys.exit()

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

    key = ""
    url = ""
    archive = False
    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-a", "--archive"):
            archive = True
        for k, v in api.items():
            if opt in (k):
                url = v
            
    if key is "":
        key = get_from_env_or_prompt('INSIGHTLY_KEY')
    if key is "":
        print "Error: Insightly key was not provided"
        sys.exit()
    if archive == True:
        today = time.strftime("%Y-%m-%dT%H:%M")
        archfile = tarfile.open("insightlybackup_%s.tar.gz" % (today), "w|gz")
        for k,v in api.items():
            url = v
            data = fetch(url, key)
            fname = url.split("/")
            fname = fname[4] + ".json"
            f = open(fname, "w")
            f.write("%s" % (data))
            f.close()
            archfile.add(fname, fname)
        archfile.close()
    else:
        data = fetch(url, key)
        if data:
            print data


if __name__ == "__main__":
    main(sys.argv[1:])

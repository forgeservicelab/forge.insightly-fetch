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

    Usage: lyfetch.py [-k <insightly_key>] [-c] [-o] [-p] [-g] [-r] [-t] [-i] [-s] [-u]

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

           -h help
    """


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hk:coapgrtisu")
    except getopt.GEtoptError:
        help()
        sys.exit()

    key = ""
    url = ""
    for opt, arg in opts:
        if opt == "-h":
            help()
            sys.exit()
        elif opt in ("-k", "--key"):
            key = arg
        elif opt in ("-c", "--contacts"):
            url = "https://api.insight.ly/v2.1/Contacts"
        elif opt in ("-o", "--organisations"):
            url = "https://api.insight.ly/v2.1/Organisations"
        elif opt in ("-p", "--projects"):
            url = "https://api.insight.ly/v2.1/Projects"
        elif opt in ("-g", "--projectcategories"):
            url = "https://api.insight.ly/v2.1/ProjectCategories"
        elif opt in ("-r", "--opportunities"):
            url = "https://api.insight.ly/v2.1/Opportunities"
        elif opt in ("-t", "--opportunitycategories"):
            url = "https://api.insight.ly/v2.1/OpportunityCategories"
        elif opt in ("-i", "--pipelines"):
            url = "https://api.insight.ly/v2.1/Pipelines"
        elif opt in ("-s", "--pipelinestages"):
            url = "https://api.insight.ly/v2.1/PipelineStages"
        elif opt in ("-u", "--opportunitystatereason"):
            url = "https://api.insight.ly/v2.1/OpportunityStateReasons"

    if key is "":
        key = get_from_env_or_prompt('INSIGHTLY_KEY')
    if key is "":
        print "Error: Insightly key was not provided"
        sys.exit()

    data = fetch(url, key)
    if data:
        print data
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])

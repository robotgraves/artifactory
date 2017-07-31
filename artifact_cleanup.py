#!/usr/bin/python

import ast
import cStringIO
import os
import pycurl

arturl = os.environ['ARTIFACTORY_URL']
artbase = os.environ['BASE_REPO']
artcount = os.environ['BASE_ARTIFACT_COUNT']
artgroup = os.environ['ARTIFACT_GROUP']
artname = os.environ['ARTIFACT_NAME']
artuser = os.environ['ARTIFACTORY_USER']
artpass = os.environ['ARTIFACTORY_PASS']
artapi = arturl + '/api'


def delete_artifact(artpath):
    artifact_url = "%s/%s" % (arturl, artpath)
    print "In queue to be deleted: " + artifact_url
    c = pycurl.Curl()
    c.setopt(pycurl.USERNAME, artuser)
    c.setopt(pycurl.PASSWORD, artpass)
    c.setopt(pycurl.URL, artifact_url)
    c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
    c.perform()
    c.close()


def list_of_artifacts_to_delete():
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "%s/search/artifact?name=%s&repos=%s" % (artapi, artname, artbase))
    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    c.setopt(pycurl.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    list_of_artifacts = ast.literal_eval(response.getvalue())
    total_artifacts = len(list_of_artifacts['results'])

    if total_artifacts > artcount:
        target = (total_artifacts - artcount) - 1  # Get the list index
        delete_artifact(list_of_artifacts['results'][target]['uri'].split("storage/")[1])

list_of_artifacts_to_delete()
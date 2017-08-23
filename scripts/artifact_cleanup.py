#!/usr/bin/python

from natsort import natsorted
import cStringIO
import json
import os
import pycurl


arturl = os.environ['ARTIFACTORY_URL']
artbase = os.environ['BASE_REPO']
artcount = int(os.environ['BASE_ARTIFACT_COUNT'])
artgroup = os.environ['ARTIFACT_GROUP']
artuser = os.environ['ARTIFACTORY_USER']
artpass = os.environ['ARTIFACTORY_PASS']
artapi = arturl + '/api'


def delete_artifact(artpath):
    artifact_url = "%s/%s/%s%s" % (arturl, artbase, artgroup, artpath)
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
    c.setopt(pycurl.URL, "%s/storage/%s/%s" % (artapi, artbase, artgroup))
    c.setopt(pycurl.CUSTOMREQUEST, 'GET')
    c.setopt(pycurl.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    data = json.loads(response.getvalue())
    artifacts_list = list()
    try:
        for artifact in data['children']:
            artifacts_list.append(str(artifact['uri']))
        artifacts_list = natsorted(artifacts_list)  # Perform a natural sort
        length = len(artifacts_list)
        while length > artcount:
            target = (length - artcount) - 1  # Get the list index
            delete_artifact(artifacts_list[target])
            length -= 1
    except KeyError:
        print "No folder to clean, given folder is empty"
        print "group = " + str(artgroup)

list_of_artifacts_to_delete()

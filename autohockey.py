#! /usr/bin/env python
#
# autohockey.py
#
# Created by Nephila (info at nephila dot it)
#
# A simple script to upload a given app to HockeyApp.
#
# -------------------------------------------------------------------------

import requests, json, sys, os.path
from requests.exceptions import ConnectionError
from optparse import OptionParser

UPLOAD_URL = 'https://rink.hockeyapp.net/api/2/apps/upload'

class AutoHockeyException(Exception): pass
class AutoHockeyConnectionError(AutoHockeyException): pass
class AutoHockeyBadFile(AutoHockeyException): pass
class AutoHockeyBadConfiguration(AutoHockeyException): pass

def upload(build_file, api_token='', dsym='', notify=2, notes=''):
    if not build_file:
        raise AutoHockeyBadConfiguration('Error! Build file not specified')
    if not os.path.exists(build_file):
        raise AutoHockeyBadFile('Error! {} build file doesn\'t exist'.format(build_file))
    if dsym and not os.path.exists(dsym):
        raise AutoHockeyBadFile('Error! {} .dsym.zip file doesn\'t exist'.format(dsym))
    params = {}
    params['dsym'] = dsym
    params['notify'] = notify
    params['notes'] = notes
    files = {'ipa': open(build_file, 'rb')}
    if dsym:
        files['dsym'] = open(options.dsym, 'rb')
    headers = {'X-HockeyAppToken' : api_token}
    try:
        req = requests.post(url=UPLOAD_URL, data=params, files=files, headers=headers)
        return (req.json(), req.status_code)
    except ConnectionError:
        raise AutoHockeyConnectionError('Connection error. Please try again.')


def main():
    usage = 'Usage: %prog [options] my_apk_or_ipa_or_app.zip_path'
    parser = OptionParser(usage=usage)
    parser.add_option( '-a', '--api-token', dest='api_token', default='', help='The API token.' )
    parser.add_option( '-s', '--dsym', dest='dsym', default='', help='iOS OSX ONLY, .dsym.zip corresponding to the build.')
    parser.add_option( '-d', '--notes', dest='notes', default='No notes', help='Your notes for this build.' )
    parser.add_option( '-n', '--notify', dest='notify', default=1, help='' )
    parser.add_option( '-c', '--config-file', dest='config_file', default='autohockey.cfg', help='Configuration file' )

    (options, args) = parser.parse_args()

    if len(args) == 0:
        parser.print_usage()
        exit(0)
    if len(args) == 1:
        build_file = args[0]

    params = {}
    params['api_token'] = options.api_token
    params['notify'] = options.notify
    params['notes'] = options.notes
    if options.config_file:
        print('Reading configuration...')
        if os.path.exists(options.config_file):
            json_file_content = open(options.config_file, 'r').read()
        else:
            print('Error! {} file doesn\'t exist'.format(options.config_file))
            exit(0)
        params = dict(list(params.items()) + list(json.loads(json_file_content).items()))

    print('Uploading file...')
    try:
        resp_json, status_code = upload(build_file, **params)
        print('Got {} from HockeyApp\n{}'.format(status_code, resp_json))
    except AutoHockeyException as ex:
        print('{}'.format(ex))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import json

import requests
import requests.cookies
import http.server
from urllib.parse import urlparse
from urllib.parse import parse_qs
import configparser

config = configparser.ConfigParser()
parser = argparse.ArgumentParser(description='Updating Styrion dns entries')
parser.add_argument('--config', type=str, help='path to config file')

# Getting the login cookie from the dashboard
def get_login(username='', password=''):
    r = requests.post('https://styrion.at/dnsadmin/', data={'username': username, 'password': password})
    if r.ok:
        print(r.cookies)
        return r.cookies['sid']


# Craft request Data and post
def update_ip(login_cookie, entry_id, domain_id, ip):
    post_data = {
        'data[0][id]': entry_id,
        'data[0][name]': 'home',
        'data[0][type]': 'A',
        'data[0][content]': ip,
        'data[0][ttl]': '300',
        'data[0][prio]': '0',
        'extra[domain_id]': domain_id,
    }
    jar = requests.cookies.RequestsCookieJar()
    jar.set('sid', login_cookie, domain='styrion.at')
    r = requests.post('https://styrion.at/dnsadmin/?a[0]=domainRecords-save', data=post_data, cookies=jar)


# Listen for get with ip parameter
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(s):
        parsed_path = urlparse(s.path)
        params = parse_qs(parsed_path.query, keep_blank_values=True)
        print('Updating Ip to ' + params['ip'][0])
        s.send_response(200)
        s.end_headers()
        login_cookie = get_login(config["Styrion"]["user"], config["Styrion"]["password"])
        for key in config["Domains"].keys():
            jsonlist = json.loads(config["Domains"][key])
            update_ip(login_cookie, jsonlist[1], jsonlist[0], params['ip'][0])
        return


if __name__ == '__main__':
    args = parser.parse_args()
    config.read(args.config)
    s = http.server.HTTPServer(('', 8000), Handler)
    s.serve_forever()

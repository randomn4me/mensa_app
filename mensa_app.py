#!/usr/bin/python3

import urllib.request

SCHEMA='http://openmensa.org/api/v2'

def get_canteens():
    request = urllib.request.urlopen('/'.join([SCHEMA, 'canteens']))
    links = request.getheader('link')
    print(links)

get_canteens()




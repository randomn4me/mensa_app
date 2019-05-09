#!/usr/bin/python3

import urllib.request
import re
import json
import argparse
import datetime


SCHEMA='https://openmensa.org/api/v2'
CANTEENS_URL = '/'.join([SCHEMA, 'canteens'])
SEPARATOR='-'*20


def get_canteens():
    request = urllib.request.urlopen(CANTEENS_URL)
    last = get_last_page(request.getheader('link'))

    all_canteens = list()
    for i in range(1, last+1):
        canteen_list = urllib.request.urlopen(f'{CANTEENS_URL}?page={i}').read()
        data = json.loads(canteen_list)
        all_canteens.extend(data)

    return all_canteens


def get_single_canteen(canteen_id):
    url = f'{CANTEENS_URL}/{canteen_id}'
    content = urllib.request.urlopen(url).read()
    data = json.loads(content)
    return data


def get_last_page(content):
    _, _, last = content.split(',')
    last_page = re.findall('<(.*?)>', last)[0]
    return int(last_page.split('=')[1])


def get_meals(canteen_id):
    iso_today = datetime.date.today().isoformat()
    url = f'{CANTEENS_URL}/{canteen_id}/days/{iso_today}/meals'

    content = urllib.request.urlopen(url).read()
    data = json.loads(content)

    return data


def filter(data, attribute, regex):
    for dp in data:
        if re.match(regex, dp[attribute], re.I):
            yield dp
    return


def pretty_print(list):
    for k, v in list:
        print(f'{k} : {v}')


ap = argparse.ArgumentParser()
ap.add_argument('-i', '--id', help='Get infos about mensa with given id')
ap.add_argument('-m', '--meals', action='store_true',
        help='Requires -i <id>: prints meals for today')
ap.add_argument('-c', '--city', help='Get infos about mensas in the given city')
ap.add_argument('name', nargs=argparse.REMAINDER,
        help='Get infos about mensas filtered by the given name')

args = ap.parse_args()

if args.id:
    canteen_data = get_single_canteen(args.id)

    if args.meals:
        print(canteen_data['name'])
        print(SEPARATOR)
        meals = get_meals(args.id)
        for m in meals:
            pretty_print([('Name', m['name']), ('Notes', m['notes'])])
            print(SEPARATOR)
    else:
        pretty_print(canteen_data.items())
elif args.city:
    canteens = get_canteens()
    for dp in filter(canteens, 'city', args.city):
        pretty_print(dp.items())
        print(SEPARATOR)
elif args.name:
    canteens = get_canteens()
    for dp in filter(canteens, 'name', ' '.join(args.name)):
        pretty_print(dp.items())
        print(SEPARATOR)
else:
    ap.print_help()

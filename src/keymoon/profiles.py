#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import rest
import argparse

def list_profiles(args):
    print "Listing Profiles:"
    profiles = rest.get("/bot", as_json=True)
    for profile in profiles:
        print "*", profile

def stop_profile(args):
    rest.delete("/bot/active")

def start_profile(args):
    rest.post("/bot/profile/" + args.profile + "/run")

def main():
    parser = argparse.ArgumentParser(description='Keymoon Profiles')

    subparsers = parser.add_subparsers(dest="command")

    subparser = subparsers.add_parser('list', help='List available profiles')
    subparser.set_defaults(func=list_profiles)

    subparser = subparsers.add_parser('stop', help='Stop active profiles')
    subparser.set_defaults(func=stop_profile)

    subparser = subparsers.add_parser('start', help='Start profiles')
    subparser.set_defaults(func=start_profile)
    subparser.add_argument('profile')

    args = parser.parse_args()

    if args.func:
        try:
            args.func(args)
        except urllib2.URLError as e:
            print "ERROR:", str(e)


if __name__ == "__main__":
    main()
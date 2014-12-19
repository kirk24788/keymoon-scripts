#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
import rest
import argparse

def list_routes(args):
    print "Listing Routes:"
    routes = rest.get("/route", as_json=True)
    for route in routes:
        print "*", route

def add_waypoint(args):
    rest.put("/routerecorder/")

def cancel(args):
    rest.delete("/routerecorder/")

def pause(args):
    rest.post("/routerecorder/pause")

def resume(args):
    rest.post("/routerecorder/resume")

def save_recording(args):
    rest.post("/routerecorder/route/" + args.route)

def start_route_recorder(args):
    if args.time <= 0:
        rest.post("/routerecorder?byDistance=" + str(args.distance))
    else:
        rest.post("/routerecorder?byInterval=" + str(args.time))

def main():
    parser = argparse.ArgumentParser(description='Route Recorder')

    subparsers = parser.add_subparsers(dest="command")

    subparser = subparsers.add_parser('list', help='List already recorder routes')
    subparser.set_defaults(func=list_routes)

    subparser = subparsers.add_parser('add', help='Add single waypoint')
    subparser.set_defaults(func=add_waypoint)

    subparser = subparsers.add_parser('start', help='Start Router Recorder')
    subparser.set_defaults(func=start_route_recorder)
    group = subparser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--distance", type=int, action="store", default=0, help="Record a waypoint every N yards")
    group.add_argument("-t", "--time", type=int, action="store", default=0, help="Record a waypoint every N milliseconds")

    subparser = subparsers.add_parser('pause', help='Pause recording')
    subparser.set_defaults(func=pause)
    subparser = subparsers.add_parser('resume', help='Resume paused recording')
    subparser.set_defaults(func=resume)
    subparser = subparsers.add_parser('cancel', help='Cancel recording')
    subparser.set_defaults(func=cancel)


    subparser = subparsers.add_parser('save', help='Save recording')
    subparser.set_defaults(func=save_recording)
    subparser.add_argument('route')

    args = parser.parse_args()

    if args.func:
        try:
            args.func(args)
        except urllib2.URLError as e:
            print "ERROR:", str(e)


if __name__ == "__main__":
    main()
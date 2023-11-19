#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (c) 2018 - 2020 Tuhinshubhra

import sys

## for people who don't bother reading the readme :/
if sys.version_info[0] < 3:
    print("\nPython3 is needed to run WP-Ateck, Try \"python3 WP-Ateck.py\" instead\n")
    sys.exit(2)

import os
import argparse
import json
import importlib

import cmseekdb.basic as cmseek # All the basic functions
import cmseekdb.core as core
import cmseekdb.createindex as createindex
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(prog='cmseek.py',add_help=False)
parser.add_argument('-h', '--help', action="store_true")
parser.add_argument('-v', '--verbose', action="store_true")
parser.add_argument("--version", action="store_true")
parser.add_argument("--update", action="store_true")
parser.add_argument('-r', "--random-agent", action="store_true")
parser.add_argument('--user-agent')
parser.add_argument('--googlebot', action="store_true")
parser.add_argument('-u', '--url')
parser.add_argument('-l', '--list')
parser.add_argument('--clear-result', action='store_true')
parser.add_argument('--follow-redirect', action='store_true')
parser.add_argument('--no-redirect', action='store_true')
parser.add_argument('--batch', action="store_true")
parser.add_argument('-i', '--ignore-cms')
parser.add_argument('--strict-cms')
parser.add_argument('--skip-scanned', action="store_true")
parser.add_argument('--light-scan', action="store_true")
parser.add_argument('-o', '--only-cms', action="store_true")
args = parser.parse_args()

if args.clear_result:
    cmseek.clear_log()

if args.help:
    cmseek.help()

if args.light_scan:
    # Suggestion #99
    cmseek.light_scan = True

if args.only_cms:
    # Suggestion #99
    cmseek.only_cms = True

if args.verbose:
    cmseek.verbose = True

if args.skip_scanned:
    cmseek.skip_scanned = True

if args.follow_redirect:
    cmseek.redirect_conf = '1'

if args.no_redirect:
    cmseek.redirect_conf = '2'

if args.update:
    cmseek.update()

if args.batch:
    #print('Batch true')
    cmseek.batch_mode = True
    print(cmseek.batch_mode)

if args.version:
    print('\n\n')
    cmseek.info("WP-Ateck Version: " + cmseek.cmseek_version)
    cmseek.bye()

if args.ignore_cms:
    cmseek.ignore_cms = args.ignore_cms.split(',')
    for acms in cmseek.ignore_cms:
        cmseek.warning('Ignoring CMS: ' + acms)

if args.strict_cms:
    cmseek.strict_cms = args.strict_cms.split(',')
    cmseek.warning('Checking target against CMSes: ' + args.strict_cms)

if args.user_agent is not None:
    cua = args.user_agent
elif args.random_agent is not None:
    cua = cmseek.randomua('random')
else:
    cua = None

if args.googlebot:
    cua = 'Googlebot/2.1 (+http://www.google.com/bot.html)'

# Update report index
index_status = createindex.init(cmseek.access_directory)
if index_status[0] != '1':
    # might be too extreme
    # cmseek.handle_quit()
    if not cmseek.batch_mode:
        input('There was an error while creating result index! Some features might not work as intended. Press [ENTER] to continue:')

if args.url is not None:
    s = args.url
    target = cmseek.process_url(s)
    if target != '0':
        if cua == None:
            cua = cmseek.randomua()
        core.main_proc(target,cua)
        cmseek.handle_quit()

elif args.list is not None:
    sites = args.list
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    sites_list = []
    try:
        with open(sites, 'r') as ot:
            file_contents = ot.read()
            if "," in file_contents:  # if comma separated URLs list
                file_contents = file_contents.replace('\n','')
                sites_list = file_contents.split(',')
            else:  # if one per line URLs list
                sites_list = file_contents.splitlines()
    except FileNotFoundError:
        cmseek.error('Invalid path! WP-Ateck is quitting')
        cmseek.bye()
    if sites_list != []:
        if cua == None:
            cua = cmseek.randomua()
        for s in sites_list:
            s = s.replace(' ', '')
            target = cmseek.process_url(s)
            if target != '0':
                core.main_proc(target,cua)
                cmseek.handle_quit(False)
                if not cmseek.batch_mode:
                    input('\n\n\tPress ' + cmseek.bold + cmseek.fgreen + '[ENTER]' + cmseek.cln + ' to continue') # maybe a fix? idk
            else:
                print('\n')
                cmseek.warning('Invalid URL: ' + cmseek.bold + s + cmseek.cln + ' Skipping to next')
        print('\n')
        cmseek.result('Finished Scanning all targets.. result has been saved under respective target directories','')
    else:
        cmseek.error("No url provided... WP-Ateck is exiting")
    cmseek.bye()

################################
###      THE MAIN MENU       ###
################################
cmseek.clearscreen()
cmseek.banner("Tip: You can use WP-Ateck via arguments as well check the help menu for more information")
print (" Input    Description")
print ("=======  ==============================")
print ("  [1]    CMS detection and Deep scan")
print ("  [2]    Scan Multiple Sites")
print ("  [3]    Bruteforce CMSs")
print ("  [U]    Update WP-Ateck")
print ("  [R]    Rebuild Cache (Use only when you add any custom module)")
print ("  [0]    Exit WP-Ateck :( \n")

selone = input("Enter Your Desired Option: ").lower()
if selone == 'r':
    cmseek.update_brute_cache()
elif selone == 'u':
    cmseek.update()
elif selone == '0':
    cmseek.bye()

elif selone == "1":
    # There goes the cms detection thingy
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    site = cmseek.targetinp("") # Get The User input
    if cua == None:
        cua = cmseek.randomua()
    core.main_proc(site,cua)
    cmseek.handle_quit()

elif selone == '2':
    cmseek.clearscreen()
    cmseek.banner("CMS Detection And Deep Scan")
    sites_list = []
    sites = input('Enter comma separated URLs without spaces (http://site1.com,https://site2.org)\nOr enter path of file containing URLs (comma separated or one-per-line):')
    if ('http' not in sites or '://' not in sites) and "," not in sites:  # because if comma in Input() then its probably comma-separated list
        cmseek.info('Treating input as path')
        try:
            with open(sites, 'r') as ot:
                file_contents = ot.read()
                if "," in file_contents:  # if comma separated URLs list
                    file_contents = file_contents.replace('\n','')
                    sites_list = file_contents.split(',')
                else:  # if one per line URLs list
                    sites_list = file_contents.splitlines()
        except FileNotFoundError:
            cmseek.error('Invalid path! WP-Ateck is quitting')
            cmseek.bye()
    else:
        cmseek.info('Treating input as URL list')
        sites_list = sites.split(',')
    if sites_list != []:
        if cua == None:
            cua = cmseek.randomua()
        for s in sites_list:
            s = s.replace(' ', '')
            target = cmseek.process_url(s)
            if target != '0':
                core.main_proc(target,cua)
                cmseek.handle_quit(False)
                if not cmseek.batch_mode:
                    input('\n\n\tPress ' + cmseek.bold + cmseek.fgreen + '[ENTER]' + cmseek.cln + ' to continue') # maybe a fix? idk
            else:
                print('\n')
                cmseek.warning('Invalid URL: ' + cmseek.bold + s + cmseek.cln + ' Skipping to next')
        print('\n')
        cmseek.result('Finished Scanning all targets.. result has been saved under respective target directories','')
    else:
        cmseek.error("No url provided... WP-Ateck is exiting")
    cmseek.bye()

elif selone == "3":
    cmseek.clearscreen()
    cmseek.banner("CMS Bruteforce Module")
    ## I think this is a modular approch
    brute_dir = os.path.join(cmseek.cmseek_dir, 'cmsbrute')
    brute_cache = os.path.join(brute_dir, 'cache.json')
    if not os.path.isdir(brute_dir):
        cmseek.error("bruteforce directory missing! did you mess up with it? Anyways WP-Ateck is exiting")
        cmseek.bye()
    else:
        print ("[#] List of CMSs: \n")
        print (cmseek.bold)
        with open(brute_cache, 'r') as read_cache:
            b_cache = read_cache.read()
        cache = json.loads(b_cache)
        brute_list = []
        for c in cache:
            brute_list.append(c)
        brute_list = sorted(brute_list)
        for i,x in enumerate(brute_list):
            n = x
            mod = "cmsbrute." + x
            exec(n + " = importlib.import_module(mod)")
            print('['+ str(i) +'] ' + cache[x])
        print(cmseek.cln + '\n')
        cmstobrute = input('Select CMS: ')
        try:
            kek = brute_list[int(cmstobrute)]
            print(kek)
            cms_brute = getattr(locals().get(kek), 'start')
            cms_brute()
        except IndexError:
            cmseek.error('Invalid Input!')
else:
    cmseek.error("Invalid Input!")
    cmseek.bye()

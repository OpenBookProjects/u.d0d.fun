# -*- coding: utf-8 -*-
'''invoke URI zipper
'''
VER = 'zipper v.21106.2042'

import os
import sys
import pickle
#import base64
#import collections
#import hashlib

#from pprint import pprint as pp
#pp = pprint.PrettyPrinter(indent=4)
#from textwrap import dedent as dedentxt

import shortuuid
shortuuid.set_alphabet("abcdefghijkmnopqrstuvwxyz0123456789+-")
from invoke import task
#import requests
from icecream import install
install()
ic.configureOutput(prefix='ic|>')

SROOT = os.path.dirname(os.path.abspath(__file__))
TPLMAP = "redirect_map.tpl"
MAPCFG = "redirect_map.conf"
MAPKL = "redirect_map.pkl"

if os.path.exists(MAPKL):
    ic('load history mapping')
    #URIMAP = pickle.load(MAPKL)
    with open(MAPKL, 'rb') as f:
        URIMAP = pickle.load(f)
else:
    ic('init. mapping')
    URIMAP = {}
    with open(MAPKL, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(URIMAP, f, pickle.HIGHEST_PROTOCOL)
#ic(URIMAP)

@task 
def ver(c):
    '''echo crt. verions
    '''
    #print(CFG.VER)
    ic(VER)
    ic(SROOT)
    #print('\n ~> powded by {} <~'.format(__version__))

#   support stuff func.
def cd(c, path2, echo=True):
    os.chdir(path2)
    if echo:
        print('\n\t crt. PATH ===')
        c.run('pwd')
        c.run('echo \n')


@task 
def add(c, url):
    '''add "URI" ~ gen. zip code for URL
    '''
    ic(url)
    #ic(shortuuid.get_alphabet())
    if url in URIMAP:
        print('already zipper this URI as:\n\t{}'.format(URIMAP[url]))
    else:
        _zip = shortuuid.ShortUUID().random(length=4)
        ic(_zip)
        URIMAP[url] = _zip
        with open(MAPKL, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(URIMAP, f, pickle.HIGHEST_PROTOCOL)
    return None


@task 
def chk(c, url):
    '''chk "URI" ~ search and echo code of URL
    '''
    ic(url)
    #ic(URIMAP)
    ic(URIMAP[url])
    return None


@task 
def upd(c, url, code):
    '''upd "URI" "code" ~ upgrade zip code of URL as give
    '''
    ic('upgrade URI mapping as')
    ic(url,code)
    URIMAP[url] = code
    with open(MAPKL, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(URIMAP, f, pickle.HIGHEST_PROTOCOL)

    return None

@task 
def exp(c):
    '''export new redirect_map.conf
    '''
    _tpl = open(TPLMAP).read()
    #ic(_tpl)
    #ic(_tpl%"/dama          https://zoomquiet.io/;")
    _cfg = ""
    _mapline = "    /{}  {};\n"
    for u in URIMAP:
        ic(u,URIMAP[u])
        _cfg += _mapline.format(URIMAP[u],u)
    #ic(_cfg)
    #return None
    open(MAPCFG,"w").write(_tpl%_cfg)
    #c.run('ls ../nginx')
    _cmd = 'cat {} > ../nginx/redirect-map.conf'.format(MAPCFG)
    ic(_cmd)
    c.run(_cmd)
    return None
    







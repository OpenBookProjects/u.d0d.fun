# -*- coding: utf-8 -*-
'''URI zipper base invoke 
gen. 4 letter code for URI;
and support:
+ upgrade point URI's code as input
+ list all zipped URI-code 
+ ...
'''
VER = 'zipper v.21107.1652'

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
    URIMAP = {"U2Z":{},"Z4U":{}}
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


def _upd_map(uri,code):
    #{"U2Z":{},"Z4U":{}}
    URIMAP['U2Z'][uri] = code
    URIMAP['Z4U'][code] = uri
    return None

def _ask_code(code):
    if code in URIMAP['Z4U']:
        return URIMAP['Z4U'][code]
    else:
        return None

def _ask_uri(uri):
    if uri in URIMAP['U2Z']:
        return URIMAP['U2Z'][uri]
    else:
        return None

@task 
def add(c, url):
    '''add "URI" ~ gen. zip code for URL
    '''
    ic(url)
    #ic(shortuuid.get_alphabet())
    _uri = _ask_uri(url)
    if _uri:
        print('already zipper this URI as:\n\t{}'.format(_uri))
    else:
        _zip = shortuuid.ShortUUID().random(length=4)
        ic(_zip)
        _upd_map(url,_zip)
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
    ic(_ask_uri(url))
    return None


@task 
def upd(c, url, code):
    '''upd "URI" "code" ~ upgrade zip code of URL as give
    '''
    ic('upgrade URI mapping as')
    ic(url,code)
    _upd_map(url,code)
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
    _mapline = "    /{}  {} ;\n"
    _exp = ""
    _ziplist = "http://u.d0d.fun/{}  {}\n"
    for u in URIMAP['U2Z']:
        #ic(u,URIMAP['U2Z'][u])
        _cfg += _mapline.format(URIMAP['U2Z'][u],u)
        _exp += _ziplist.format(URIMAP['U2Z'][u],u)
    #ic(_cfg)
    print(_exp)
    #return None
    open(MAPCFG,"w").write(_tpl%_cfg)
    #c.run('ls ../nginx')
    _cmd = 'cat {} > ../nginx/redirect-map.conf'.format(MAPCFG)
    ic(_cmd)
    c.run(_cmd)
    return None
    







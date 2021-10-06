# -*- coding: utf-8 -*-
'''invoke URI zipper
'''
VER = 'zipper v.210902.2055'

import os
import sys
import base64
import collections
import hashlib

from pprint import pprint as pp
#pp = pprint.PrettyPrinter(indent=4)
from textwrap import dedent as dedentxt

from invoke import task
#import requests
from icecream import install
install()
ic.configureOutput(prefix='ic|>')

SROOT = os.path.dirname(os.path.abspath(__file__))

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
def exp(c):
    '''export new redirect_map.conf
    '''
    _tpl = open('redirect_map.tpl').read()
    ic(_tpl)
    ic(_tpl%"/dama          https://zoomquiet.io/;")
    open('redirect_map.conf',"w").write(_tpl%"/dama          https://zoomquiet.io/;")
    


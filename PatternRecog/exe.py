# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:51:36 2019

@author: mr_ro
"""

from cx_Freeze import setup, Executable

base = None    

executables = [Executable("SocketServer.py", base=base)]

packages = ["socket"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "sever",
    options = options,
    version = "1.0",
    description = 'none',
    executables = executables
)
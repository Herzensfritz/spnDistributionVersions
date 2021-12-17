#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""   This program can be used to create and/or update a json-file that describes the different versions of angular distributions. 
"""
#    Copyright (C) University of Basel 2021  {{{1
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/> 1}}}

__author__ = "Christian Steiner"
__maintainer__ = __author__
__copyright__ = 'University of Basel'
__email__ = "christian.steiner@unibas.ch"
__status__ = "Development"
__license__ = "GPL v3"
__version__ = "0.0.1"

import getopt
import json
import os
from os import listdir, sep, path, setpgrp, devnull
from os.path import exists, isfile, isdir, dirname, basename
import re
import sys

def add_version(json_file: str, version_dir: str, versionName: str):
    """Add version to json file.
    """
    if isdir(version_dir):
        versionNumber = version_dir.replace(sep, '')
        data_list = []
        if isfile(json_file):
            with open(json_file) as infile:
                data_list = json.load(infile)
        data = {}
        if len([ data for data in data_list if data['number'] == versionNumber ]) > 0:
            data = [ data for data in data_list if data['number'] == versionNumber ][0]
        else:
            data_list.append(data)
        data.update({ 'name': versionName})
        data.update({ 'number': version_dir.replace(sep, '')})
        scripts = [ { 'src': script, 'isModule': re.match(r'.*[0-9]{4}.js', script) is not None } for script in listdir(version_dir) if script.endswith('.js') ]
        data.update({ 'scripts': scripts})
        with open(json_file, 'w') as outfile:
            json.dump(data_list, outfile)
    else:
        msg = f'Error: directory {version_dir} does not exist!' 
        raise Exception(msg);

def usage():
    """prints information on how to use the script
    """
    print(main.__doc__)

def main(argv):
    """This program can be used to create and/or update a json-file that describes the different versions of angular distributions.

    addVersion.py [OPTIONS] <jsonFile> <versionDirectory> ...
        
        <jsonFile>              the target json file.
        <versionDirectory>      the angular distribution directory for which a version information should be generated.

        OPTIONS:
        -h|--help                           show help
        -a|--alpha-version=versionDirectory indicates that versionDirectory is a alpha version.
        -b|--beta-version=versionDirectory  indicates that versionDirectory is a beta version.
    
        :return: exit code (int)
    """
    alpha_beta_dict = {}
    try:
        opts, args = getopt.getopt(argv, "ha:b:", ["help", "alpha=", "beta="])
    except getopt.GetoptError:
        usage()
        return 2
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            return 0
        elif opt in ('-a', '--alpha'):
            alpha_beta_dict.update({ arg: 'Alpha-Version'})
        elif opt in ('-b', '--beta'):
            alpha_beta_dict.update({ arg: 'Beta-Version'})
    exit_status = 0
    if len(args) < 2:  
        usage()
        return 2
    json_file = args[0]
    for version_dir in args[1:]:
        versionNumber = version_dir.replace(sep, '')
        version_name = alpha_beta_dict[versionNumber]\
                if bool(alpha_beta_dict.get(versionNumber))\
                else 'Version'
        add_version(json_file, version_dir, version_name)
    return exit_status

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

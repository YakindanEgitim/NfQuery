# This file is part of NfQuery.  NfQuery is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright NfQuery Team Members

#!/usr/local/bin/python

import datetime
import os
import sys 
import simplejson as json

# importable functions 
__all__ = ['fetch_source', 'parse_source']

def fetch_source(source_link, source_file):
    try:
        os.system("fetch -o " + source_file + " " + source_link)
    except Exception, e:
        os.system("wget " + source_link + " -O " + source_file)

def parse_source_and_create_output(source_name, source_file, output_type, output_file):
    '''
        Malc0de Parser
    ''' 
    
    update_time = datetime.datetime.now()
    update_time = update_time.strftime("%Y-%m-%d %H:%M")
    
    output = ''

    try:
        source = open(source_file,"r")
        outputfile = open(output_file, "w")
    except Exception, e:
        print 'Exception'
        sys.exit(1)

    # parse the file line by line and create an ip list
    expr_list = []
    for line in source.readlines()[4:]:
        ip = line.split("\n")[0]
        expr_list.append({'src_ip' :  ip})

    # JSON
    json_dict = [
                 {
                  'source_name' : source_name,
                  'date' : update_time,
                  'mandatory_keys' : ['src_ip'],
                  'expr_list' : expr_list
                 }
                ]
    #print json_dict
    outputfile.write(json.dumps(json_dict, indent=4))

    outputfile.close()
    source.close()


if __name__ == "__main__":
    print 'calling main'

    # making parameter assignments manually for now.


    #source_link = 'http://malc0de.com/bl/IP_Blacklist.txt'
    #source_file = '/usr/local/nfquery/sources/malc0de/malc0deSource.txt'
    #output_type = 1 # Ip list
    #output_file = '/usr/local/nfquery/sources/malc0de/malc0deOutput.txt'

    #fetch_source(source_link, source_file)
    #parse_source_and_create_output(source_name, source_file, output_type, output_file)
    
    source_name = 'malc0de'
    source_link = 'http://malc0de.com/bl/IP_Blacklist.txt'
    source_dir  =  os.path.dirname(__file__)
    print source_dir
    source_file = source_dir + './malc0deSource.txt'
    output_type = 1 # Ip list
    output_file = source_dir + './malc0deOutput.txt'

    #fetch_source(source_link, source_file)
    try:
        parse_source_and_create_output(source_name, source_file, output_type, output_file)
    except Exception, e:
        print e

    
    

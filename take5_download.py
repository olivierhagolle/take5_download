#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Author O.Hagolle, CESBIO and CNES

import json
import time
import os, os.path, optparse,sys
from datetime import date

###########################################################################
class OptionParser (optparse.OptionParser):
 
    def check_required (self, opt):
      option = self.get_option(opt)
 
      # Assumes the option's 'default' is set to None!
      if getattr(self.values, option.dest) is None:
          self.error("%s option not supplied" % option)
 
###########################################################################

#==================
#parse command line
#==================
if len(sys.argv) == 1:
    prog = os.path.basename(sys.argv[0])
    print '      '+sys.argv[0]+' [options]'
    print "     Aide : ", prog, " --help"
    print "        ou : ", prog, " -h"
    print "example 1 : python %s -s 'ToulouseFrance' -a auth_theia.txt -d 2015-04-01 -f 2015-04-18 -l LEVEL2A"%sys.argv[0]
    sys.exit(-1)
else :
    usage = "usage: %prog [options] "
    parser = OptionParser(usage=usage)
  
    parser.add_option("-s","--site", dest="site", action="store", type="string", \
            help="site name",default=None)		
    parser.add_option("-a","--auth_theia", dest="auth_theia", action="store", type="string", \
            help="Theia account and password file")
    parser.add_option("-w","--write_dir", dest="write_dir", action="store",type="string",  \
            help="Path where the products should be downloaded",default='.')
    parser.add_option("-c","--collection", dest="collection", action="store", type="choice",  \
            help="SPOT4 or SPOT5",choices=['SPOT4','SPOT5'],default='SPOT5')
    parser.add_option("-l","--level", dest="level", action="store", type="choice",  \
            help="LEVEL1C or LEVEL2A",choices=['LEVEL1C','LEVEL2A'],default=None)
    parser.add_option("-n","--no_download", dest="no_download", action="store_true",  \
            help="Do not download products, just print curl command",default=False)
    parser.add_option("-d", "--start_date", dest="start_date", action="store", type="string", \
            help="start date, fmt('2015-12-22')",default=None)
    parser.add_option("-f","--end_date", dest="end_date", action="store", type="string", \
            help="end date, fmt('2015-12-23')",default=None)

    (options, args) = parser.parse_args()

if options.level!=None:
    level="\&processingLevel=%s"%options.level
else:
    level=""
    
if options.start_date!=None:    
    start_date=options.start_date
    if options.end_date!=None:
        end_date=options.end_date
    else:
        end_date=date.today().isoformat()



#====================
# read authentification file
#====================
try:
    f=file(options.auth_theia)
    (email,passwd)=f.readline().split(' ')
    if passwd.endswith('\n'):
        passwd=passwd[:-1]
    f.close()
except :
    print "error with password file"
    sys.exit(-2)


#============================================================
# get a token to be allowed to bypass the authentification.
# The token is only valid for two hours. If your connection is slow
# or if you are downloading lots of products, it might be an issue
#=============================================================

get_token='curl -k -s -X POST --data-urlencode "ident=%s" --data-urlencode "pass=%s" https://theia.cnes.fr/services/authenticate/>token.json'%(email,passwd)

os.system(get_token)

with open('token.json') as data_file:
    try :
        token_json = json.load(data_file)
    except :
        print "Authentification is probably wrong"
        sys.exit(-1)
    token=token_json["access_token"]

#====================
# search catalogue
#====================

if os.path.exists('search.json'):
    os.remove('search.json')
    
search_catalog='curl -k -o search.json https://spot-take5.org/resto/api/collections/%s/search.json?\&zone_geo=%s\&startDate=%s\&completionDate=%s%s\&maxRecords=500'%(options.collection,options.site,start_date,end_date,level)
print search_catalog
os.system(search_catalog)
time.sleep(10)


#====================
# Download
#====================

with open('search.json') as data_file:    
    data = json.load(data_file)

for i in range(len(data["features"])):    
    print data["features"][i]["properties"]["productIdentifier"],data["features"][i]["id"],data["features"][i]["properties"]["startDate"]
    prod=data["features"][i]["properties"]["productIdentifier"]
    feature_id=data["features"][i]["id"]
    if options.write_dir==None :
        get_product='curl -o %s.zip -k -H "Authorization: Bearer %s" https://spot-take5.org/resto/collections/%s/%s/download/?issuerId=theia'%(prod,token,options.collection,feature_id)
    else :
        get_product='curl -o %s/%s.zip -k -H "Authorization: Bearer %s" https://spot-take5.org/resto/collections/%s/%s/download/?issuerId=theia'%(options.write_dir,prod,token,options.collection,feature_id)
    print get_product
    if not(options.no_download):
        os.system(get_product)


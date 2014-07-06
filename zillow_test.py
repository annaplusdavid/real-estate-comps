import urllib
import urllib2
import xmltodict
import json
import csv
import os, sys

zillowkey = 'X1-ZWz1b5h21e7ax7_2ox88'
truliakey = '3vk72hc66u3jv4z7qr9pvxzf'

# ---------------------------------------------
# Concatenate parameters into a query string
# ---------------------------------------------
def queryStringize ( parms, parmArray ):
  queryString  = "&".join( [ item+'='+urllib.quote_plus(parms[item]) for item in parmArray ] )
  return queryString


# ---------------------------------------------
# Get Search Results
#http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=<ZWSID>&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA
# ---------------------------------------------
def getSearchResults (address, city):
  url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?'

  parms = {
    'zws-id':zillowkey, 
    'address':address,
    'citystatezip':city, 
    'output':'json'
  }

  parmArray = []
  parmArray.append('zws-id')
  parmArray.append('address')
  parmArray.append('citystatezip')
  parmArray.append('output')

  urlout = url + queryStringize(parms, parmArray)
  print urlout

  response = urllib2.urlopen(urlout).read()
  return response

# ---------------------------------------------
# Parse Search Results
# ---------------------------------------------
def parseSearchResults (response):
  
  listing = {}

  content = xmltodict.parse(response)
  #print json.dumps(content, indent=4)
  
  #get the zpid
  status = content["SearchResults:searchresults"]['message']['code']
  print "parse search: " + content["SearchResults:searchresults"]['message']['text']
  
  if status != '0':
    return
  else:
    result = content["SearchResults:searchresults"]['response']['results']['result']
    listing = parseResult(result)
  return listing

# ---------------------------------------------
# Parse Search Result
# ---------------------------------------------

def parseResult (result):
  listing = {}

  listing['z-link'] = result['links']['homedetails']
  listing['zpid'] = result['zpid']
  listing['street'] = result['address']['street']
  listing['zipcode'] = result['address']['zipcode']
  listing['city'] = result['address']['city']
  listing['state'] = result['address']['state']
  listing['lat'] = result['address']['latitude']
  listing['long'] = result['address']['longitude']

  #check for useCode for search
  listing['useCode'] = result['useCode'] if 'useCode' in result else '' 

  listing['lotSizeSqFt'] = result['lotSizeSqFt'] if 'lotSizeSqFt' in result else '' 
  listing['bathrooms'] = float(result['bathrooms']) if 'bathrooms' in result else '' 
  listing['bedrooms'] = result['bedrooms'] if 'bedrooms' in result else '' 

  listing['neighborhood_type'] = result['localRealEstate']['region']["@type"]
  if result['localRealEstate']['region']["@type"]:
    listing['neighborhood'] = result['localRealEstate']['region']["@name"]

  listing['z-amount'] = result['zestimate']['amount']['#text']
  listing['z-high'] = result['zestimate']['valuationRange']['high']['#text']
  listing['z-low'] = result['zestimate']['valuationRange']['low']['#text']

  #check for comparables 
  listing['finishedSqFt'] = result['finishedSqFt'] if 'finishedSqFt' in result else '' 
  listing['lastSoldDate'] = result['lastSoldDate'] if 'lastSoldDate' in result else ''


  return listing

# ---------------------------------------------
# Get Comparables
#http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=<ZWSID<&zpid=48749425&count=5
# ---------------------------------------------
def getComparables (zpid, num):
  url = 'http://www.zillow.com/webservice/GetDeepComps.htm?'

  num = str(num)

  parms = {
    'zws-id':zillowkey,
    'zpid':zpid,
    'count':num,
    'output':'json'
  }

  parmArray = []
  parmArray.append('zws-id')
  parmArray.append('zpid')
  parmArray.append('count')
  parmArray.append('output')

  urlout = url + queryStringize(parms, parmArray)

  response = urllib2.urlopen(urlout).read()
  return response
  #searchResults = json.loads(response)

# ---------------------------------------------
# Parse Search Results
# ---------------------------------------------
def parseComparables (response):
  comps = []


  content = xmltodict.parse(response)
  #print json.dumps(content, indent=4)
  
  #get the zpid
  status = content["Comps:comps"]['message']['code']
  print "parse comparables: " + content["Comps:comps"]['message']['text']
  
  if status == '0':
    #get comparables
    results = content["Comps:comps"]['response']['properties']['comparables']

    for listing in results['comp']:
      comp = {}
      comp = parseResult(listing)
      comps.append(comp)
  
  return comps



# ---------------------------------------------
# Get List of Neighborhoods 
# http://api.trulia.com/webservices.php?library=LocationInfo&function=getNeighborhoodsInCity&city=San Francisco&state=CA&apikey=abc123
# ---------------------------------------------
def getNeighborhoods ():
  url = 'http://api.trulia.com/webservices.php/?'
  parms = {
    'library':'LocationInfo',
    'function':'getNeighborhoodsInCity',
    'city':'San Francisco',
    'state':'CA',
    'apikey':apikey
  }

  parmArray = []
  parmArray.append('library')
  parmArray.append('function')
  parmArray.append('city')
  parmArray.append('state')
  parmArray.append('apikey')

  urlout = url + queryStringize(parms, parmArray)

  response = urllib2.urlopen(urlout).read()
  return response

# ---------------------------------------------
# Get Neighborhood Stats
#http://api.trulia.com/webservices.php?library=TruliaStats&function=getNeighborhoodStats
#&neighborhoodId=1386&startDate=2009-02-06&endDate=2009-02-07&apikey=abc123
# ---------------------------------------------
def getNeighborhoodStats ( neighborhoodId, startDate, endDate ):
  url = 'http://api.trulia.com/webservices.php?'
  parms = {
    'library':'TruliaStats', 
    'function':'getNeighborhoodStats', 
    'neighborhoodId': neighborhoodId, 
    'startDate': startDate,
    'endDate': endDate, 
    #statType options {all, traffic, listings}
    'statType': 'listings',
    'apikey': truliakey
  }

  parmArray = []
  parmArray.append('library')
  parmArray.append('function')
  parmArray.append('neighborhoodId')
  parmArray.append('startDate')
  parmArray.append('endDate')
  parmArray.append('statType')
  parmArray.append('apikey')

  urlout = url + queryStringize(parms, parmArray)

  response = urllib2.urlopen(urlout).read()
  return response


# ---------------------------------------------
# Main
# ---------------------------------------------

def main():
  address = sys.argv[1]
  
  #returns
  response = getSearchResults(address, 'San Francisco, CA')
  listing = parseSearchResults(response)

  #15079081
  #find comparables
  response = getComparables(listing['zpid'], 25)
  #comps is an array of comparables
  comps = parseComparables(response)
  subcomps = []

  for item in comps: 
    response = getComparables(item['zpid'], 3)
    subcomps.extend( parseComparables(response) )
    #comps.extend(subcomps)
    #print item.items()

  print comps[0].keys()

  for item in comps:
    print item.values()
  
  for item in subcomps:
    print item.values()

if __name__ == "__main__":
  main()

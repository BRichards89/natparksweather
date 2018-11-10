import requests

def MakeOptions(appendString, validKeys, requiredKeys, options):
    for key,value in options.items():
        if key in validKeys:
            appendString = appendString + "?{}={}".format(key,value)
        else:
            print('{} is not a valid option!'.format(key))
    return appendString

def RequestData(**kwargs):
    validKeys = ['datasetid', 'datatypeid', 'locationid', 'stationid', 'startdate', 'enddate', 'units', 
                'sortfield', 'sortorder', 'limit', 'offset','includemetadata']
    requiredKeys = ['datasetid','startdate','enddate']
    return  MakeOptions('data', validKeys, requiredKeys,  kwargs)

def RequestDataCategories(**kwargs):
    validKeys = ['datasetid', 'locationid', 'stationid', 'startdate', 'enddate', 'sortfield', 'sortorder', 'limit', 'offset']
    appendString = "datacategories"
    for key,value in kwargs.items():
        if key in validKeys:
            appendString = appendString + "?{}={}".format(key,value)
        else:
            print('{} is not a valid option!'.format(key)) 
    return appendString


def main(accessToken):
    baseURL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
    # Example 
    # response = requests.get(baseURL + "stations",headers={'token': accessToken})
    # print(response.text)
    #response = requests.get(baseURL + "stations?locationid=FIPS:51", headers={'token': accessToken})
    #response = requests.get(baseURL + "stations?locationid=FIPS:51", headers={'token': accessToken})
    #response = requests.get(baseURL + "locationcategories?limit=1000", headers={'token': accessToken}).json()
#    response = requests.get(baseURL + "datacategories?limit=1000", headers={'token': accessToken}).json()
#    for i in range(len(response['results'])): print(response['results'][i]['name'])
    strRequest = baseURL + RequestData(limit="1000",testKey='999')
    print(strRequest)
    response = requests.get(strRequest, headers={'token': accessToken})
    print(response.text)
    jResponse = response.json()
    for i in range(len(jResponse['results'])): print(jResponse['results'][i]['name'])

main(accessToken)

import requests
import os.path

def GetAccessToken():
    print('Reading configuration settings..', end='')
    if os.path.isfile('conf.ini'):
        with open('conf.ini', 'r') as confFile:
            for line in confFile.readlines():
                confSetting = line.replace(' ', '').rstrip('\n\r').replace('{', '').replace('}', '').split(":")
                if confSetting[0] == 'accessToken':
                    print('..Access token found!')
                    return confSetting[1]
    else:
        print('..No configuration found! Creating conf.ini.')
        with open('conf.ini', 'w') as confFile:
            confFile.write('{accessToken} : {}')
    return ""

def MakeOptions(appendString, validKeys, requiredKeys, options):
    if set(requiredKeys).issubset(list(options.keys())):
        for key,value in options.items():
            if key in validKeys:
                appendString = appendString + "?{}={}".format(key,value)
            else:
                print('{} is not a valid option!'.format(key))
    else:
        appendString = 'Missing required arguments (' + \
                       ', '.join([missingKey for missingKey in requiredKeys if missingKey not in list(options.keys())]) \
                       + ') for \"' + appendString + '\" API call.'
    return appendString

def RequestData(**kwargs):
    validKeys = ['datasetid', 'datatypeid', 'locationid', 'stationid', 'startdate',
                 'enddate', 'units', 'sortfield', 'sortorder', 'limit', 'offset',
                 'includemetadata']
    requiredKeys = ['datasetid', 'startdate', 'enddate']
    return MakeOptions('data', validKeys, requiredKeys,  kwargs)

def RequestDataCategories(**kwargs):
    validKeys = ['datasetid', 'locationid', 'stationid', 'startdate', 'enddate',
                 'sortfield', 'sortorder', 'limit', 'offset']
    requiredKeys = []
    return MakeOptions('datacategories', validKeys, requiredKeys, kwargs)

def RequestDatasets(**kwargs):
    validKeys = ['datatypeid', 'locationid', 'stationid', 'startdate', 'enddate',
                 'sortfield', 'sortorder', 'limit', 'offset']
    requiredKeys = []
    return MakeOptions('datasets', validKeys, requiredKeys, kwargs)

def main(accessToken):
    baseURL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
    # Example 
    # response = requests.get(baseURL + "stations",headers={'token': accessToken})
    # print(response.text)
    # response = requests.get(baseURL + "stations?locationid=FIPS:51", headers={'token': accessToken})
    # response = requests.get(baseURL + "stations?locationid=FIPS:51", headers={'token': accessToken})
    # response = requests.get(baseURL + "locationcategories?limit=1000", headers={'token': accessToken}).json()
#    response = requests.get(baseURL + "datacategories?limit=1000", headers={'token': accessToken}).json()
#    for i in range(len(response['results'])): print(response['results'][i]['name'])
    #strRequest = RequestData(limit="1000",testKey='999')
    # strRequest = RequestDataCategories(limit='1000')
    strRequest = RequestDatasets(limit='1000')
    if 'Missing required arguments' not in strRequest:
        response = requests.get(baseURL + strRequest, headers={'token': accessToken})
        print(response.text)
        jResponse = response.json()
        for i in range(len(jResponse['results'])):
            print(jResponse['results'][i]['name'] + ' : ', end='')
            print(jResponse['results'][i]['id'])
    else:
        print(strRequest)


accessToken = GetAccessToken()
if accessToken == '':
    print("Please insert API token into conf.ini and try again!")
else:
    main(accessToken)

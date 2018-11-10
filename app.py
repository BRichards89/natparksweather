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


def MakeRequest(apiArg, apiDict, options):
    if set(apiDict[apiArg][1]).issubset(list(options.keys())):
        appendString = apiArg
        for key, value in options.items():
            if key in apiDict[apiArg][0]:
                appendString = appendString + "?{}={}".format(key, value)
            else:
                print('{} is not a valid option!'.format(key))
    else:
        appendString = 'Missing required arguments (' + \
                       ', '.join(
                           [missingKey for missingKey in apiDict[apiArg][1] if missingKey not in list(options.keys())]) \
                       + ') for \"' + apiArg + '\" API call.'
    return appendString


def BuildAPIDictionary():
    # Build our dictionary for API calls.
    # API lives here: https://www.ncdc.noaa.gov/cdo-web/webservices/v2
    # Key = api call type
    # Value = [valid keys],[required keys]
    apiDict = dict()
    apiDict['datasets'] = [['datatypeid', 'locationid', 'stationid', 'startdate', 'enddate',
                            'sortfield', 'sortorder', 'limit', 'offset'],
                           []]
    apiDict['datacategories'] = [['datasetid', 'locationid', 'stationid', 'startdate', 'enddate',
                                  'sortfield', 'sortorder', 'limit', 'offset'],
                                 []]
    apiDict['datatypes'] = [['datasetid', 'locationid', 'stationid', 'datacategoryid', 'startdate',
                             'enddate', 'sortfield', 'sortorder', 'limit', 'offset'],
                            []]
    apiDict['locationcategories'] = [['datasetid', 'startdate', 'enddate', 'sortfield', 'sortorder', 'limit', 'offset'],
                                     []]
    apiDict['locations'] = [['datasetid', 'locationcategoryid', 'datacategoryid', 'startdate', 'enddate',
                             'sortfield', 'sortorder', 'limit', 'offset'],
                            []]
    apiDict['stations'] = [['datasetid', 'locationid', 'datacategoryid', 'datatypeid', 'extent',
                            'startdate', 'enddate', 'sortfield', 'sortorder', 'limit', 'offset'],
                           []]
    apiDict['data'] = [['datasetid', 'datatypeid', 'locationid', 'stationid', 'startdate',
                        'enddate', 'units', 'sortfield', 'sortorder', 'limit', 'offset',
                        'includemetadata'],
                       ['datasetid', 'startdate', 'enddate']]

    return apiDict


def main(accessToken):
    # set where the API lives. Thanks NOAA!
    baseURL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"
    # Build the API dictionary of valid / required keys for each lookup type
    apiDict = BuildAPIDictionary()
    # What options do we want in our query? This will get moved out of main method / main method will be removed once
    # this is ported to an actual app thing
    options = dict()
    options['limit'] = '1000'
    # Make our request
    strRequest = MakeRequest('data', apiDict, options)
    # Check if we have a valid (no missing arguments) request
    if 'Missing required arguments' not in strRequest:
        # If we have a valid request, send it
        response = requests.get(baseURL + strRequest, headers={'token': accessToken})
        print(response.text)
        jResponse = response.json()
        for i in range(len(jResponse['results'])):
            print(jResponse['results'][i]['name'] + ' : ', end='')
            print(jResponse['results'][i]['id'])
    else:
        # We don't have a valid request. What are we missing?
        print(strRequest)


accessToken = GetAccessToken()
if accessToken == '':
    print("Please insert API token into conf.ini and try again!")
else:
    main(accessToken)

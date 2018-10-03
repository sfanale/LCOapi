""" This will be a template program to experiment with LCO Api implementation
Just Schedule for now!
Notes:
  Submit telemetry for SOAR saying it is available for scheduling
HTTP POST to https://telemetry-api-beta.lco.global/api/telemetry
The json body of the POST request should look like:
[{"first_timestamp": "2018-09-05T14:41:05Z", "last_timestamp": "2018-09-05T14:46:43Z", "site": "sar", "name": "AVAILABLE_FOR_SCHEDULING", "value": “true”}]
Get the schedule of requests for SOAR:
https://request-api-beta.lco.global/api/schedule?site=sar
Update state of scheduled request when beginning observation
HTTP PATCH to https://request-api-beta.lco.global/api/configurationstatus/2
The ID at the end should come from the configuration_status id field
The json body of the PATCH request should be {"state": "ATTEMPTED"}
The configuration should be returned with the new state shown
Parse a request into macro commands
Update the state of scheduled request when observation is over
HTTP Patch to https://request-api-beta.lco.global/api/configurationstatus/2
The json body of the PATCH should update both the state (to COMPLETED or FAILED), and the event structure:
{"state": "COMPLETED", "event": { "start": "2018-09-05T00:00:15Z", "end": "2018-09-05T00:33:12Z", "state": "DONE", "reason": "", "time_completed": 1855, "events": [] } }
6.	Queue the data product file for archive ingestion
HTTP POST to https://archive-api-beta.lco.global/api/ingest
The json body is an array of URI’s to data products



to get the test script
schedule = requests.get('https://request-api-beta.lco.global/api/schedule?site=sar')
schedule = schedule.json()

"""

import requests


#http://observe.lco.global/api/schedule
dict = "get_schedule, Exit"


def main():
    element = None
    creds= None
    while element != "Exit":
        element, queue = dequeue_element(queue)

        if element == None:
            command = poll()
            queue = enqueue_element(queue, command)

        elif element == "help":
            print(dict)

        elif element == "init":
            creds= auth()

        elif element == "get_schedule":
            schedule= get_schedule(creds)
            schedule.json()

        elif element == "Exit":
            return None
        else:
            return None
    return None


def poll():
    command = input('Enter desired command:')
    return command


def enqueue_element(queue, element):
    queue.append(element)
    return queue


def dequeue_element(queue):
    try:
        element = queue[0]
        queue = queue[1:]
    except IndexError:
        element = None
        queue = []
    return element, queue


def auth():
    # need a username and password
    creds= request.get('http://observe.lco.global/api/api-token-auth/')
    return creds

def user_request():
    r = requests.post('http://observe.lco.global/api/userrequests',data, json )


def get_schedule(creds):
    # get the schedule using site info
    # header Authorization = Token {API_TOKEN}.
    #  headers = {'user-agent': 'my-app/0.0.1'}
    # payload = {'site': "", 'observatory': "", 'telescope': "", 'request_id': 10, 'userrequest_id': 100, 'limit': 1}
    # headers = {'Authorization': "APIKEY"}
    schedule = requests.get('https://request-api-beta.lco.global/api/schedule?site=sar')
    schedulej=schedule.json()
    config = schedulej['results'][0]['request']['configurations'][0]['instrument_config']
    gssConfig = toGSS(config)
    return schedule

gssTemplate = {"SI camera info":
                   {"Observer Name":"name","object name":"object_name","File name base":"file_name",
                    "Camera Color":"Red","Exp type tab":"Object","Number of Exp":1,"Exp time":1,"CCD Readout Speed":1,
                    "CCD ROI Mode":9,"Hg(Ar)":False,"Cu":False,"Ne":False,"Bulb":False,"Ar":False,"Quartz":False,
                    "Quartz Percent":0,"Fe":False,"Notes":"","Target Number":"","DomePercent":0,
                    "Dome":False,"Start":0,"Delta":0,"Steps":0,
                    "Custom Roi":
                        {"0":0,"1":4192,"2":1,"3":1800,"4":200,"5":2}},
               "Configuration":
                   {"Primary Filter":"<NO FILTER>","Secondary Filter":"<NO FILTER>","Slit Mask":"<NO SLIT>",
                    "Grating":"<NO GRATING>","CS Target":0,"GS Target":0,"Coll Focus":1000,"Camera Focus":0,
                    "Name":"setup_name","User":"","Date":"","Comment":"","use Flexure Comp?":True,"Select Mode:":34},
               "RA (HH:MM:SS.SS)":"-00:00:00.00","DEC (HH:MM:SS.SS)":"-00:00:00.00"}


def toGSS(config): # take an array of instrument configurations and build basic config script
    # TODO add the target information to part of this unless SOM wants to control that
    length = len(config)
    # TODO convert RA and DEC from degrees to HH:MM:SS.ss
    # TODO EQUINOX is always a standard default ICRS
    # TODO PARALAC angle - yes or no - Goes to the TCS - could be paralac angle or IPA angle
    # TODO ADCSTAT - yes or no - Goes to TCS - if you arent at paralac you want ADC
    # We are going to combine Paralac and ADC
    # TODO PARALAC TRUE MAPS TO TO ROTMODE VFLOAT AND THEN PARALAC FALSE IS SKY
    # TODO ROTANGLE IS IPA, ONLY MATTERS IF ROTMODE IS SKY
    # TODO IF ROTMODE IS VFLOAT THE PARALAC IS TRUE AND ADC IS OUT
    # TODO COMP MIRROR IS IN OR OUT BASED ON OBSTYPE AND LAMP STATUS - WE INFER THIS ON THIS SIDE
    # TODO GRATING, PF, SF, SLIT FROM OPTICAL_PARAMS - WE ARE LAUNCHING WITH JUST 400 GRATING
    # TODO WAVELENGTH MODE - LAUNCHING WITH 400 M1 AND 400 M2
    # Maybe offer modes as "gratings" on the LCO side
    # f1, f2, and slit will be string names
    # null fields of no field should be <no filter>
    # TODO LAMPS WILL BE IN EXTRA PARAMS AS LAMP NAME ON/OFF
    # TODO QUARTZ AND DOME PERCENT - WONT BE INCLUDED - FREEZE TO ?
    # These types of cals should be done in the afternoon not by users as night
    # Hg(Ar) and Ne are the two we are launching with
    # TODO WE THINK WE CAN REMOVE LAMP KEYWORDS AND JUST INFER FROM OBSTYPE AND SETUP
    # Focus should be determined in the afternoon callibrations
    # Camera color, this shouldn't be relevant
    # might offer different grating modes for different camera colors
    # TODO TYPE FILED WILL MAP TO READOUT MODE AND ROI (SPEC 1X1 OR 2X2 AND 344,3) - SPECTRUM
    # IMAGING DEFAULT WILL BE (IMAGING 2X2, 750,2
    # TODO TYPE FIELD SHOULD DISTINGUISH FROM SPECTRUM, LAMP_FLAT, EXPOSE (IMAGING)
    # FILENAME STANDARD = LONG FILE NAMES FROM LCO



    gssScript = [gssTemplate]*length

    for index, setup in enumerate(config):
        if setup['optical_elements']['filters'] is not None:
            gssScript[index]['Configuration']['Primary Filter'] = setup['optical_elements']['filters']
        if setup['optical_elements']['secondary_filters'] is not None:
            gssScript[index]['Configuration']['Secondary Filter'] = setup['optical_elements']['secondary_filters']
        if setup['optical_elements']['gratings'] is not None:
            gssScript[index]['Configuration']['Grating'] = setup['optical_elements']['gratings']
        if setup['optical_elements']['slits'] is not None:
            gssScript[index]['Configuration']['Slit Mask'] = setup['optical_elements']['slits']
        gssScript[index]['Configuration']['Select Mode']
        gssScript[index]['SI camera info']['Observer Name'] = 'LCO'
        gssScript[index]['SI camera info']['object name'] = setup['name']
        gssScript[index]['SI camera info']['File name base']
        gssScript[index]['SI camera info']['Exp type tab']
        gssScript[index]['SI camera info']['Number of Exp'] = setup['exposure_count']
        gssScript[index]['SI camera info']['Exp time'] = setup['exposure_time']
        gssScript[index]['SI camera info']['CCD Readout Speed'] = setup['readout_mode']
        gssScript[index]['SI camera info']['CCD ROI Mode']
        #gssScript[index]['SI camera info']['Custom Roi']





response = {'count': 4, 'next': None, 'previous': None, 'results': [
        {'cancel_date': '', 'configuration_status': [
            {'camera_code': 'gman01', 'configuration': 2, 'event': {}, 'id': 2, 'modified': '2018-08-30T20:41:05Z',
             'state': 'FAILED'}],
         'end': '2018-09-07T11:41:05Z', 'group_id': 'my observations on target',
         'id': 2, 'ipp_value': 1.05, 'modified': '2018-08-30T20:41:05Z', 'observation_type': 'NORMAL',
         'observatory': 'doma', 'priority': 30, 'proposal': 'LCO2018B-014', 'reason': 'Configuration Timed out',
         'request':
             {'acceptability_threshold': 90, 'completed': '', 'configurations': [
                 {'acquisition':
                      {'acquire_radius_arcsec': 3, 'extra_params': {}, 'mode': 'ON', 'name': '',
                       'strategy': 'BRIGHTEST'},
                  'args': '', 'constraints':
                      {'max_airmass': 1.6, 'min_lunar_distance': 30},
                  'guiding':
                      {'exposure_time': 10, 'extra_params': {}, 'filter': '', 'mode': 'ON', 'name': '',
                       'strategy': 'CATALOGUE'},
                  'id': 2, 'instrument_config': [
                     {'bin_x': 1, 'bin_y': 1, 'exposure_count': 3, 'exposure_time': 150,
                      'extra_params': {}, 'filter': 'I', 'name': '4M0-GOODMAN-SCICAM-RED',
                      'readout_mode': '', 'rot_angle': 0, 'rot_mode': 'SKY'}],
                  'priority': 1, 'target':
                      {'dec': -22.1884, 'epoch': 2000, 'extra_params': {}, 'name': 'My Target',
                       'ra': 34.24231, 'type': 'ICRS'},
                  'type': 'SPECTRUM'}],
              'created': '2018-08-30T20:41:05Z', 'duration': 948, 'fail_count': 0, 'id': 2,
              'modified': '2018-08-30T20:41:05Z', 'observation_note': 'A Basic SOAR Observation',
              'state': 'PENDING'},
         'site': 'sar', 'start': '2018-09-07T10:41:05Z', 'state': 'FAILED', 'submitter': 'username3',
         'telescope': '4m0a'}
    ]}







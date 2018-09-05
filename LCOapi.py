""" This will be a template program to experiment with LCO Api implementation
Just Schedule for now!
Notes:
    1)This API uses API keys for authentication. The easiest way to use it is to get the api key from your profile or via
     the /api-token-auth/ endpoint using your username and password. Then submit all api requests with the header
     Authorization = Token {API_TOKEN}.

     2)http://observe.lco.global/api/userrequests
        {
        "requests": [
        {}
        ],
        "group_id": "A Short Description",
        "observation_type": "NORMAL",
        "operator": "SINGLE",
        "ipp_value": 1.05,
        "proposal": "LCOEPA2018B-002"
        }



    3) http://observe.lco.global/api/schedule, [str site, str observatory, str telescope,str start_after,
            str start_ before, str end_after, end_before, str modified after, str(enum) order ("start"|"modified")
            int request_id, int userrequest_id, str(enum) state("PENDING"|"ABORTED"|"CANCELLED"|"COMPLETED"),
            int limit, int offset]

        {
        "count": 1,
        "next": "http://observe.lco.global/api/schedule/?params=...&offset=...",
        "previous": null,
        "results": [
        {}
        ]
        }


    payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
    r.json()
"""

import requests


#http://observe.lco.global/api/schedule

def main():



def auth():



def user_request():
    r = requests.post('http://observe.lco.global/api/userrequests',data, json )



def get_schedule():
    # get the schedule using site info
    payload= { 'site': "", 'observatory': "", 'telescope': "", 'request_id': 10, 'userrequest_id': 100, 'limit':1 }
    schedule = requests.get('http://observe.lco.global/api/schedule',payload)
    schedule.json()
    return schedule








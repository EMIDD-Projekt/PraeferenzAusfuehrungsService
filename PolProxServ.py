"""
Policy Proxy Service

is used to enforce privacy preferences or generalized usage policies for external datasets
"""
from flask import Flask, request, jsonify
from werkzeug.wrappers import Response
import requests
import json
import yappl


app = Flask(__name__)


def get_preference(url):
    r = requests.get(url)
    return r.content


def getHour(timestamp):
    date, time = timestamp.split('T')
    daytime, offset = time.split('.')
    hour, minute, second = daytime.split(':')
    return hour


def getDay(timestamp):
    date, time = timestamp.split('T')
    year, month, day = date.split('-')
    return day


def hourlyTimestamp(timestamp):
    date, time = timestamp.split('T')
    daytime, offset = time.split('.')
    hour, minute, second = daytime.split(':')
    minute = '00'
    second = '00'
    offset = '00Z'
    newTimestamp = date + 'T' + hour + ':' + minute + ':' + second + '.' + offset
    return newTimestamp


def dailyTimestamp(timestamp):
    date, time = timestamp.split('T')
    daytime, offset = time.split('.')
    hour, minute, second = daytime.split(':')
    hour = '00'
    minute = '00'
    second = '00'
    offset = '00Z'
    newTimestamp = date + 'T' + hour + ':' + minute + ':' + second + '.' + offset
    return newTimestamp


def average(valueList):
    if len(valueList) < 1:
        return 0
    else:
        sum = 0
        for value in valueList:
            sum = sum + value
        return sum / len(valueList)


def minmax(valueList):
    if len(valueList) < 1:
        return [0, 0]
    else:
        min = valueList[0]
        max = valueList[0]
        for value in valueList:
            if value < min:
                min = value
            if value > max:
                max = value
        return [min, max]


@app.route("/")
def simple_proxy():
    incoming = str(request.full_path)
    r = requests.get('https://www.opensense.network/' + incoming, verify=False)
    return Response(r.content, mimetype=r.headers['Content-Type'])


@app.route("/<path:query>")
def opensense_proxy(query):

    incoming = str(request.full_path)
    incomming_url, incomming_args = incoming.split('?')

    if incomming_url[-6:] == 'values':
        bypass = 'False'
    else:
        bypass = 'True'

    if bypass == 'True':
        r = requests.get('https://www.opensense.network/' + incoming, verify=False)
        return Response(r.content, mimetype=r.headers['Content-Type'])

    if incomming_url[-12:] == '/v1.0/values':
        allSensorProxy = 'True'
        opensense_url = 'https://www.opensense.network/beta/api/v1.0/values?'
    else:
        oneSensorProxy = 'True'
        sensorID, values = incomming_url[-12:].split('/')
        opensense_url = 'https://www.opensense.network/beta/api/v1.0/sensors/' + sensorID + '/values?'

    r = requests.get(opensense_url + incomming_args, verify=False)

    utilizer = []
    purpose = []

    if len(incomming_args) < 2:
        return '403 - data access prohibit without proper declaration of utilizer and desired processing purpose.'
    params = incomming_args.split('&')
    for param in params:
        par, val = param.split('=')
        if par == 'utilizer':
            if val not in utilizer:
                utilizer.append(val)
        if par == 'purpose':
            if val not in purpose:
                purpose.append(val)

    if len(utilizer) > 1:
        return '403 - only one utilizer per request allowed'
    if len(purpose) > 1:
        return '403 - only one purpose per request allowed'

# --- for .../sensors/{sensorID}/values queries only --- #

    if oneSensorProxy == 'True':
        sensorData = json.loads(r.content)

        preference_link = sensorData['usagePreferenceLink']
        preference = get_preference(preference_link)
        preference = yappl.parse(preference)

        sensorValues = sensorData['values']

        if utilizer[0] in preference.getExcludedUtilizer():
            return '403 - data access prohibit - excluded utilizer'
        if purpose[0] in preference.getExcludedPurpose():
            return '403 - data access prohibit - excluded purpose'

        trRules = preference.getTrRules()
        for rule in range(len(trRules)):

            if utilizer[0] in trRules[rule]['Utilizer']:
                if purpose[0] in trRules[rule]['Purpose']:
                    trans = trRules[rule]['Transformation']
                    transFu = []
                    for i in range(len(trans)):
                        transFu.append(trans[i]['tr_func'])
                    transFu = transFu[0]  # TODO: quick'n dirty hack 4 single value sensors --> revise!!!
                    func, intervall = transFu.split('_')

                    retval = {}
                    retval['accuracy'] = sensorData['accuracy']
                    retval['altitudeAboveGround'] = sensorData['altitudeAboveGround']
                    retval['attributionText'] = sensorData['attributionText']
                    retval['attributionURL'] = sensorData['attributionURL']
                    retval['directionHorizontal'] = sensorData['directionHorizontal']
                    retval['directionVertical'] = sensorData['directionVertical']
                    retval['id'] = sensorData['id']
                    retval['licenseId'] = sensorData['licenseId']
                    retval['location'] = sensorData['location']
                    retval['measurandId'] = sensorData['measurandId']
                    retval['sensorModel'] = sensorData['sensorModel']
                    retval['unitId'] = sensorData['unitId']
                    retval['usagePreferenceLink'] = sensorData['usagePreferenceLink']
                    retval['userId'] = sensorData['userId']

                    values2send = []

                    if intervall == 'hourly':
                        start = getHour(sensorValues[0]['timestamp'])
                        hourValuesTimestamp = hourlyTimestamp(sensorValues[0]['timestamp'])
                        hourValues = []
                        for value in sensorValues:
                            if str(getHour(value['timestamp'])) == start:
                                hourValues.append(value['numberValue'])
                            else:
                                if func == 'average':
                                    hourValue = average(hourValues)
                                    hourValue2send = {}
                                    hourValue2send['timestamp'] = hourValuesTimestamp
                                    hourValue2send['numberValue'] = hourValue
                                    values2send.append(hourValue2send)

                                    start = getHour(value['timestamp'])
                                    hourValues = []
                                    hourValuesTimestamp = hourlyTimestamp(value['timestamp'])

                                elif func == 'minmax':
                                    hourValue = minmax(hourValues)
                                    hourValue2send0 = {}
                                    hourValue2send1 = {}
                                    hourValue2send0['timestamp'] = hourValuesTimestamp
                                    hourValue2send0['numberValue'] = hourValue[0]
                                    values2send.append(hourValue2send0)
                                    hourValue2send1['timestamp'] = hourValuesTimestamp
                                    hourValue2send1['numberValue'] = hourValue[1]
                                    values2send.append(hourValue2send1)

                                    start = getHour(value['timestamp'])
                                    hourValues = []
                                    hourValuesTimestamp = hourlyTimestamp(value['timestamp'])
                                else:
                                    return '500 - internal server error'

                    elif intervall == 'daily':
                        start = getDay(sensorValues[0]['timestamp'])
                        dayValuesTimestamp = dailyTimestamp(sensorValues[0]['timestamp'])
                        dayValues = []
                        for value in sensorValues:
                            if str(getDay(value['timestamp'])) == start:
                                dayValues.append(value['numberValue'])
                            else:
                                if func == 'average':
                                    dayValue = average(dayValues)
                                    dayValue2send = {}
                                    dayValue2send['timestamp'] = dayValuesTimestamp
                                    dayValue2send['numberValue'] = dayValue
                                    values2send.append(dayValue2send)

                                    start = getDay(value['timestamp'])
                                    dayValues = []
                                    dayValuesTimestamp = dailyTimestamp(value['timestamp'])

                                elif func == 'minmax':
                                    dayValue = minmax(dayValues)
                                    dayValue2send0 = {}
                                    dayValue2send1 = {}
                                    dayValue2send0['timestamp'] = dayValuesTimestamp
                                    dayValue2send0['numberValue'] = dayValue[0]
                                    values2send.append(dayValue2send0)
                                    dayValue2send1['timestamp'] = dayValuesTimestamp
                                    dayValue2send1['numberValue'] = dayValue[1]
                                    values2send.append(dayValue2send1)

                                    start = getDay(value['timestamp'])
                                    dayValues = []
                                    dayValuesTimestamp = dailyTimestamp(value['timestamp'])
                                else:
                                    return '500 - internal server error'

                    else:
                        return '400 - bad request'

                    retval['values'] = values2send
                    return jsonify(retval)

                else:
                    errormsg = '403 - data access prohibit - no valid purpose'
            else:
                errormsg = '403 - data access prohibit - no valid utilizer'

        if errormsg:
            return errormsg
        else:
            return jsonify(retval)

    else:
        return '500 - internal server error'
# --- for .../sensors/values queries --- #

    """
    generate a list of sensordata containing sensor id and usagePreferenceLink
    """
    #  TODO: finish this!

    sensors = json.loads(r.content)
    preference_links = []
    sensor_nr = 0
    for sensor in sensors:
        preference_link = {}
        preference_link['id'] = sensors[sensor_nr]['id']
        preference_link['usagePreferenceLink'] = sensors[sensor_nr]['usagePreferenceLink']
        sensor_nr = sensor_nr + 1
        preference_links.append(preference_link)
#    return jsonify(attribution_links)
#  ---
    sensor_preferences = []
    preference_nr = 0
    for link in preference_links:
        sensor_preference = {}
        sensor_preference['id'] = preference_links[preference_nr]['id']
        sensor_preference['policy'] = json.loads(get_preference(preference_links[preference_nr]['id'], preference_links[preference_nr]['preferenceURL']))
        sensor_preferences.append(sensor_preference)
        preference_nr = preference_nr + 1
    return jsonify(sensor_preferences)
#  ---


if __name__ == '__main__':
    app.run()
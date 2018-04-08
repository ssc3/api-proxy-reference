from flask import Blueprint, jsonify, request, redirect, url_for

import logging
import requests
import json
import random
import uuid
import time
import os
import subprocess

sse_proxy_bp = Blueprint('sse_proxy_bp', __name__)


SSE = "OBFUSCATED"
API_PROXY = "OBFUSCATED"
SSE_ORG_ID = "OBFUSCATED"
SSE_REGISTRY = "OBFUSCATED"
SSE_REGISTRY = "OBFUSCATED"
SSE_REGISTRY_DEVICEID = "OBFUSCATED"


globalSession = None

responseMsg = {
    "status": "success",
    "code": 200,
    "msg": "",
    "body": {}
}

sseMsgBody = {"headers":
            {"version": "1.0", "messageId": "", "authHeader":
                {"auth":
                    {"keyId": "1234",
                    "encAlg": "Alg",
                    "encHash":
                        {"ct": "Ct",
                        "tag": "HashTag",
                        "iv": "Iv"},
                    "signature": "array that includes H"}}},
        "payload": [{"scheme": "http",
                     "operation": "POST",
                    "command": "http://127.0.0.1/bingopy",
                    "commandId": "1234",
                    "timeout": 5,
                    "body": {
}}]}
 
 
sseMsgPayload = {"scheme": "http",
                     "operation": "POST",
                    "command": "http://172.17.0.1/bingopy",
                    "commandId": "1234",
                    "timeout": 5,
                    "headers": {},
                    "body": {}
}





def successJsonResponse(aInStatusCode=200, aInMsg=None, **aInDict):
    global responseMsg

    if len(aInDict) != 0:
        responseMsg['body'] = aInDict
    else:
        responseMsg['body'] = {}

    if aInMsg is None:
        responseMsg['msg'] = ''
    else:
        responseMsg['msg'] = str(aInMsg)

    responseMsg['code'] = aInStatusCode
    responseMsg['status'] = 'success'

    return jsonify(responseMsg)

def failJsonResponse(aInStatusCode=400, aInMsg=''):
    global responseMsg

    responseMsg['body'] = {}
    responseMsg['code'] = aInStatusCode
    responseMsg['status'] = 'fail'
    responseMsg['msg'] = aInMsg

    return jsonify(responseMsg)


'''
UTIL FUNCTIONS
'''

def generateUrl(*args):
    url = "".join([*args])
    return url
 
def executeRequest(session, aInMethod, aInProxyUrl, aInBody=None):
    if aInMethod.lower() == "get":
        logging.debug("Executing GET: " + aInProxyUrl)
        res = session.get(aInProxyUrl)
    elif aInMethod.lower() == "post":
        logging.debug("Executing POST: " + aInProxyUrl)
        res = session.post(aInProxyUrl, data=json.dumps(aInBody))

    return res

'''
Literally create a session with a connector device
Does not create a global session with SSE
'''

def getDevices(aInSession):
    deviceUrl = generateUrl(SSE, SSE_REGISTRY, 'machine-name') # should be hostname
    deviceUrl = generateUrl(SSE, SSE_REGISTRY) # should be hostname
    logging.info("EXECUTE REQUEST: " + deviceUrl)
    lResponse = aInSession.get(deviceUrl)
    logging.debug(json.dumps(lResponse.json(), indent=4))
    return lResponse

def getSpecificDeviceInfo(aInSession, aInDeviceId):
    deviceUrl = generateUrl(SSE, SSE_REGISTRY_DEVICEID, aInDeviceId) # should be hostname
    logging.info("EXECUTE REQUEST: " + deviceUrl)
    lResponse = aInSession.get(deviceUrl)
    logging.debug(json.dumps(lResponse.json(), indent=4))
    return lResponse


def getSseSession():
    global globalSession

    if globalSession:
        return globalSession

    else:
        logging.info("SSE: Creating session with SSE")
        globalSession = requests.Session()
        globalSession.cert = ("cert.pem", "certs.key")
        globalSession.headers.update({"Content-Type": "application/json"})
        
        
        return globalSession

def executeCommand(aInSession, aInDeviceId, aInUri, aInMsgPayload=None, aInMethod='GET', aInPayloadScheme='http'):

    global sseMsgPayload
    global sseMsgBody

    logging.info("Here")

    sseMsgPayload["scheme"] = "http"
    sseMsgPayload["operation"] = aInMethod
    sseMsgPayload["command"] = aInPayloadScheme+"://localhost:80/" + "v1/apic/" + aInUri
    sseMsgPayload["commandId"] = "1234"
    sseMsgPayload["timeout"] = 300
    sseMsgPayload["body"] = {}

    logging.info("Here2")

    #if aInDeviceId in deviceToApicTokenMap:
    #    sseMsgPayload["headers"]['Cookie'] = "APIC-Cookie=" + deviceToApicTokenMap.get(aInDeviceId)

    proxy_url = generateUrl(SSE, API_PROXY, SSE_ORG_ID, "/", aInDeviceId, "?mode=inline")
    msgId=int(random.randrange(1000))
    logging.info("Here3")
    sseMsgBody["headers"]["messageId"] = str(msgId) #str(random.randrange(1000))
    sseMsgBody["payload"][0] = sseMsgPayload
    sseMsgBody["payload"][0]["commandId"] = str(random.randrange(1000))

    command_res = executeRequest(aInSession, "POST", proxy_url, sseMsgBody)
    logging.debug("**************** SEND COMMAND3 O/P ***************")
    logging.debug(command_res.text)
    command_output = command_res.json()["payload"][0]["body"]
    logging.debug("**************** SEND COMMAND3 O/P JSON ***************")
    logging.debug(json.dumps(command_output, indent=4))
    return command_res


@sse_proxy_bp.route('/', methods=['GET'])
def sseIndex():
    return "In Bp"


@sse_proxy_bp.route('/devices', methods=['GET'])
def getAllDevices():
    try:
        lSession = getSseSession()

        lResponseDict = {}

        lResponse = getDevices(lSession)

        lResponseDict = lResponse.json()

        return successJsonResponse(200, aInMsg=None, aInDict=lResponseDict)

    except:
        return failJsonResponse(400, aInMsg="Fetching all devices unsuccessful")


@sse_proxy_bp.route('/devices/<string:deviceId>', methods=['GET'])
def getSpecificInfo(deviceId):
    try:
        if deviceId == "":
            return redirect(url_for('getAllDevices'))
        else:
            lSession = getSseSession()

            lResponse = getSpecificDeviceInfo(lSession, deviceId)

            lResponseDict = lResponse.json()

            return successJsonResponse(200, aInMsg=None, aInDict=lResponseDict)

    except:
        return failJsonResponse(400, aInMsg="Could not fetch specific info for this device")





@sse_proxy_bp.route('/devices/<string:deviceId>/machine/<path:machineUri>', methods=['GET', 'POST'])
def executeApicRequest(deviceId, apicUri):

    try:
        lSession = getSseSession()

        logging.info('GOT SESSION')


        lResponseDict = {}

        logging.info('Got apic request: ' + str(request.query_string))

        if request.method.lower() == 'POST'.lower():
            logging.info("Executing POST")
            lRequestBody = request.get_json(silent=True)
            lResponse = executeCommand(aInSession=lSession, aInDeviceId=deviceId, aInUri=machineUri, aInMsgPayload=json.loads(lRequestBody), aInMethod='POST', aInPayloadScheme='http')
            lResponseDict = json.loads(lResponse.json())["payload"][0]["body"]

        else:
            logging.info("Executing GET")
            lResponse = executeCommand(aInSession=lSession, aInDeviceId=deviceId, aInUri=machineUri, aInMethod='GET', aInPayloadScheme='http')
            lResponseDict = lResponse.json()["payload"][0]["body"]

        return successJsonResponse(200, aInMsg=None, aInDict=lResponseDict)

    except:
        return failJsonResponse(400, aInMsg="Could not execute Machine request")








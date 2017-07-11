import configparser
import json
import apiai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

CONFIG = configparser.ConfigParser()
CONFIG.read('keys.cfg')

# Twilio account info
account_sid = CONFIG['TWILIO']['ACCOUNT_SID']
auth_token = CONFIG['TWILIO']['AUTH_TOKEN']
account_num = CONFIG['NUMBERS']['TWILIO']
client = Client(account_sid, auth_token)

# api.ai account info
CLIENT_ACCESS_TOKEN = CONFIG['APIAI']['ACCESS_TOKEN']
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():
    # get SMS input via twilio
    resp = MessagingResponse()

    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = msg

    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        if response_obj["result"]["actionIncomplete"]:
            response = response_obj["result"]["fulfillment"]["speech"]
            # send SMS response back via twilio
            client.messages.create(to=msg_from, from_= account_num, body=response)
        else:
            fitness_class = response_obj["result"]["parameters"]["class"]
            location = response_obj["result"]["parameters"]["location"]
            date = response_obj["result"]["parameters"]["date"]
            parameters = "Class: {}, Location: {}, Date: {}".format(fitness_class, location, date)
            
            client.messages.create(to=msg_from,
                                   from_=account_num,
                                   body=parameters)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
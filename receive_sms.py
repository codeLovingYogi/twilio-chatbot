from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse().message("Hello, Mobile Monkey")
    return str(resp)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    resp = MessagingResponse().message("How can we help you?")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
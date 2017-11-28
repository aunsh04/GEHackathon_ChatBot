from twilio import twiml
import nltk
from flask import Flask, request
import urllib2
from twilio.rest import TwilioRestClient
import requests
from response import get_response
import pyowm


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def hello():
	in_text = request.form["Body"]
	ph_number = request.form["From"]
	in_text = in_text.lower()
	out_text = get_response(in_text)
	response = twiml.Response()
	response.message(out_text)
	return str(response)

if __name__ == "__main__":
	app.run(debug=True)
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import json
import requests
import redis
from tasks import process_sms
from constants import Config

redis_client = redis.from_url(Config.redis_url)

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.values)
    incoming_msg = request.values.get('Body', '').lower()
    message_from = request.values.get('From', '')
    process_sms.delay(message_from, incoming_msg)
    response_msg = "Typing"
    
    resp = MessagingResponse()
    resp.message(response_msg)

    return Response(str(resp), mimetype="application/xml")     
 

if __name__ == '__main__':
    app.run(debug=True)
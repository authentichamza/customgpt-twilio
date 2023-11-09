from flask import Flask, request, make_response
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
    incoming_msg = request.values.get('Body', '').lower()
    message_from = request.values.get('From', '')
    process_sms.delay(message_from, incoming_msg)
    response_msg = make_response("OK", 200)

    return response_msg

if __name__ == '__main__':
    app.run(debug=True)
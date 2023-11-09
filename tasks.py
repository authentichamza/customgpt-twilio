from celery import Celery
from twilio.rest import Client
from constants import Config
import json
import requests
app = Celery(
    'tasks',
    broker=Config.redis_url,
    backend=Config.redis_url
)
api_endpoint = Config.api_endpoint
project_id = Config.project_id
twilio_phone_number = Config.twilio_phone_number

headers = {
  'Authorization': f"Bearer {Config.api_key}",
  'Content-Type': 'application/json'
}
# Initialize Twilio client
client = Client(Config.account_sid, Config.auth_token)

@app.task
def process_sms(recipient_phone_number, message_body):
  message_body = generate_response(message_body)
  message = client.messages.create(
      body=message_body,
      from_=twilio_phone_number,
      to=recipient_phone_number
  )

def generate_response(message_body):
  url = api_endpoint + 'projects/' + str(project_id) + '/conversations'

  payload = json.dumps({
      "name": "Twilio Conversation"
  })

  create_conversation = requests.request("POST", url, headers=headers, data=payload)
  conversation_data = json.loads(create_conversation.text)["data"]
  session_id = conversation_data["session_id"]
  url = api_endpoint + 'projects/' + str(project_id) + '/conversations/' + str(session_id) + '/messages'
  payload = json.dumps({
    "prompt": message_body
  })
  response = requests.request("POST", url, headers=headers, data=payload)
  response_customgpt = json.loads(response.text)['data']
  openai_response = response_customgpt['openai_response']
  return openai_response

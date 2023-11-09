from celery import Celery
from twilio.rest import Client
from constants import Config
import json
import requests
import redis
# Import SDK if you dont want to use api directly
from customgpt_client import CustomGPT

redis_client = redis.from_url(Config.redis_url)

app = Celery(
    'tasks',
    broker=Config.redis_url,
    backend=Config.redis_url
)
api_endpoint = f"#{Config.base_url}/api/v1"
project_id = Config.project_id
twilio_phone_number = Config.twilio_phone_number

# API Set headers
headers = {
  'Authorization': f"Bearer {Config.api_key}",
  'Content-Type': 'application/json'
}
# CustomGPT SDK configurations if SDK
CustomGPT.api_key = Config.api_key
CustomGPT.base_url = Config.base_url

# Initialize Twilio client
client = Client(Config.account_sid, Config.auth_token)

@app.task
def process_sms(recipient_phone_number, message_body):
  #Using SDK
  message_body = generate_response_via_sdk(recipient_phone_number, message_body)
  # Using API uncomment below
  # message_body = generate_response_via_api(recipient_phone_number, message_body)
  message = client.messages.create(
      body=message_body,
      from_=twilio_phone_number,
      to=recipient_phone_number
  )

def generate_response_via_api(recipient_phone_number, message_body):
  url = api_endpoint + 'projects/' + str(project_id) + '/conversations'

  payload = json.dumps({
      "name": "Twilio Conversation"
  })
  session_id = redis_client.get(recipient_phone_number)
  if not session_id:
    create_conversation = requests.request("POST", url, headers=headers, data=payload)
    conversation_data = json.loads(create_conversation.text)["data"]
    session_id = conversation_data["session_id"]
    redis_client.set(recipient_phone_number, session_id)

  url = api_endpoint + 'projects/' + str(project_id) + '/conversations/' + str(session_id) + '/messages'
  payload = json.dumps({
    "prompt": message_body
  })
  response = requests.request("POST", url, headers=headers, data=payload)
  response_customgpt = json.loads(response.text)['data']
  openai_response = response_customgpt['openai_response']
  return openai_response

def generate_response_via_sdk(recipient_phone_number, message_body):
  session_id = redis_client.get(recipient_phone_number)
  if not session_id:
    create_conversation = CustomGPT.Conversation.create(project_id=project_id, name='Twilio')
    conversation_data = create_conversation.parsed.data
    session_id = conversation_data.session_id
    redis_client.set(recipient_phone_number, session_id)

  response = CustomGPT.Conversation.send(project_id=project_id, session_id=session_id, prompt=message_body)
  response_customgpt = response.parsed.data
  openai_response = response_customgpt.openai_response
  return openai_response


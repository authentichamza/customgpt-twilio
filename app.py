from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import json
import requests
load_dotenv()

app = Flask(__name__)

# Set your OpenAI API key
api_key = os.environ.get('CUSTOMGPT_API_KEY')
api_endpoint = os.environ.get('CUSTOMGPT_BASE_URL') or "https://app.customgpt.ai/api/v1/"
project_id = os.environ.get('CUSTOMGPT_PROJECT_ID')

headers = {
  'Authorization': f"Bearer {api_key}",
  'Content-Type': 'application/json'
}
@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.values)
    incoming_msg = request.values.get('Body', '').lower()
    response_msg = generate_response(incoming_msg)
    
    resp = MessagingResponse()
    resp.message(response_msg)

    return Response(str(resp), mimetype="application/xml") 

def generate_response(user_input):
    url = api_endpoint + 'projects/' + str(project_id) + '/conversations'

    payload = json.dumps({
        "name": "Twilio Conversation"
    })

    create_conversation = requests.request("POST", url, headers=headers, data=payload)
    conversation_data = json.loads(create_conversation.text)["data"]
    session_id = conversation_data["session_id"]
    url = api_endpoint + 'projects/' + str(project_id) + '/conversations/' + str(session_id) + '/messages'
    payload = json.dumps({
      "prompt": user_input
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    response_customgpt = json.loads(response.text)['data']
    openai_response = response_customgpt['openai_response']
    return openai_response
 

if __name__ == '__main__':
    app.run(debug=True)
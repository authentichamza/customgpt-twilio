from dotenv import load_dotenv
import os
load_dotenv()

class Config:
	redis_url = os.environ.get('REDIS_URL')
	account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
	auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
	twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
	api_key = os.environ.get('CUSTOMGPT_API_KEY')
	api_endpoint = os.environ.get('CUSTOMGPT_BASE_URL') or "https://app.customgpt.ai/api/v1/"
	project_id = os.environ.get('CUSTOMGPT_PROJECT_ID')


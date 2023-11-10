# Twilio Chatbot with CustomGPT

This project integrates Twilio for SMS messaging with a CustomGPT-powered chatbot.

## Setup

1. **Clone the repository:**

   ```bash
   git clone git@github.com:authentichamza/customgpt-twilio.git
   cd customgpt-twilio
   ```

2. **Create a `.env` file in the project root and add the following environment variables:**

   ```dotenv
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   CUSTOMGPT_API_KEY=your_customgpt_api_key
   CUSTOMGPT_PROJECT_ID=your_customgpt_project_id
   REDIS_URL=your_redis_url
   TWILIO_PHONE_NUMBER=your_twilio_phone_number
   ```

3. **If Docker is available, use:**

   ```bash
   docker build .
   docker run -p 127.0.0.1:8000:8000 {docker_build_id}
   ```

   **Otherwise, install Python 3.8:**
   And install
   ```bash
   apt-get install -y redis-server
   ```
   ```bash
   pip install -r requirements.txt
   run redis-server --daemonize yes && gunicorn -b 0.0.0.0:8000 --reload app:app & celery -A tasks worker -P threads --loglevel=debug
   ```

4. **After running the app, host it on ngrok or any domain.**

5. **Configure Twilio:**
	 - Get you AUTH_TOKEN and ACCOUNT_SID from twilio dashboard.
   - Go to Twilio Messaging Services, create a new service or use the default, and navigate to Integrations.
   - Select "Send to Webhook" and set your webhook URL to `{YOUR_DOMAIN}/webhook` in Twilio.
   - In Twilio Phone Numbers, activate your number and copy it to the `TWILIO_PHONE_NUMBER` environment variable.
   - In the phone number configuration, under messaging, select the service for SMS that has your webhook URL set.

Now your Twilio Chatbot with CustomGPT is set up and running!

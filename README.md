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
   REDIS_URL=redis://localhost:6379
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
   - Get you AUTH_TOKEN and ACCOUNT_SID and PHONENUMBER from twilio dashboard and add it to .env.
   ![Screenshot from 2023-11-10 05-42-26](https://github.com/authentichamza/customgpt-twilio/assets/43203240/f7d65213-d8b9-478f-aa32-398656eb3b54)
   - Go to Twilio Messaging Services, create a new service or use the default, and navigate to Integrations.
   ![Screenshot from 2023-11-10 05-43-49](https://github.com/authentichamza/customgpt-twilio/assets/43203240/fe6586cf-c4a7-458d-844b-9494a06d643a)
   - Select "Send to Webhook" and set your webhook URL to `{YOUR_DOMAIN}/webhook` in Twilio.
   ![Screenshot from 2023-11-10 05-44-07](https://github.com/authentichamza/customgpt-twilio/assets/43203240/8a43174d-6b5c-4d24-8fbe-d8e0fcd509ae) 
   - Go to phone number > active numbers > {SELECT A PHONE NUMBER} than in the phone number configuration, under messaging, select the service for SMS that has your webhook URL set.

Now your Twilio Chatbot with CustomGPT is set up and running!


from flask import Flask, request, make_response
from tasks import process_sms
from constants import Config

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    message_from = request.values.get('From', '')
    # Run Background worker to process response
    process_sms.delay(message_from, incoming_msg)
    response_msg = make_response("OK", 200)

    return response_msg

if __name__ == '__main__':
    app.run(debug=True)
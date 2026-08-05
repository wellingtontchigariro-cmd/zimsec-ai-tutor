from flask import Flask, request, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO) # add this at top

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # VERIFY for Meta setup
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            logging.info("WEBHOOK VERIFIED")
            return request.args.get('hub.challenge')
        else:
            logging.warning("VERIFY_TOKEN MISMATCH")
            return 'Wrong token', 403

    # RECEIVE MESSAGES
    if request.method == 'POST':
        logging.info("POST RECEIVED") # <--- THIS IS THE KEY LINE
        logging.info(f"DATA: {request.get_json()}") # <--- AND THIS ONE
        
        # Always reply 200 to Meta or it will retry
        return jsonify({"status": "ok"}), 200
    
    return 'Method not allowed', 405

@app.route('/health')
def health():
    return jsonify({"status":"ok"})

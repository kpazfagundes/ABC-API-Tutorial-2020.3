# Copyright 2016-2020 Apple, Inc.
# All Rights Reserved.

import requests
import uuid

from config import BIZ_ID, BUSINESS_CHAT_SERVER
from jwt_util import get_jwt_token


def send_text_message(destination_id, message_text):
    message_id = str(uuid.uuid4())  # generate unique message id

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % get_jwt_token(),
        "id": message_id,
        "Source-Id": BIZ_ID,
        "Destination-Id": destination_id
    }

    payload = {
        "body": message_text,
        "sourceId": BIZ_ID,
        "locale": "en_US",
        "destinationId": destination_id,
        "v": 1,
        "type": "text",
        "id": message_id
    }

    r = requests.post("%s/message" % BUSINESS_CHAT_SERVER,
                      json=payload,
                      headers=headers,
                      timeout=10)

    print("Business Chat server return code: %s" % r.status_code)


if __name__ == "__main__":
    destination_id = "<source_id from previously received message>"
    send_text_message(destination_id, "Greetings from your CSP!")

# Expected output:
# Business Chat server return code: 200

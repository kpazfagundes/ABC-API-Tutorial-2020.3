# Copyright 2016-2020 Apple, Inc.
# All Rights Reserved.

import requests
import uuid

from config import BIZ_ID, BUSINESS_CHAT_SERVER, IMESSAGE_EXTENSION_BID
from jwt_util import get_jwt_token


def send_time_picker_with_user_timezone(destination_id):
    # here we are sending a time picker with a localized time depending on the user's timezone
    # devices with different timezone settings will display different times

    message_id = str(uuid.uuid4())  # generate unique message id

    # a unique request id that will be sent back with response
    request_id = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer %s" % get_jwt_token(),
        "id": message_id,
        "Source-Id": BIZ_ID,
        "Destination-Id": destination_id
    }

    interactive_data = {
        "bid": IMESSAGE_EXTENSION_BID,
        "data": {
            "mspVersion": "1.0",
            "requestIdentifier": request_id,
            "event": {
                "identifier": "1",
                "title": "",
                "timeslots": [
                    {
                        "duration": 3600,
                        "startTime": "2020-12-15T17:00+0000",
                        "identifier": "0"
                    }
                ]
            }
        },
        "receivedMessage": {
            "style": "icon",
            "title": "Please pick a time",
            "subtitle": "This should be 10:00am for -7h users"
        },
        "replyMessage": {
            "style": "icon",
            "title": "Thank you!"
        }
    }

    payload = {
        "type": "interactive",
        "interactiveData": interactive_data,
        "sourceId": BIZ_ID,
        "destinationId": destination_id,
        "v": 1,
        "id": message_id
    }

    r = requests.post("%s/message" % BUSINESS_CHAT_SERVER,
                      json=payload,
                      headers=headers,
                      timeout=10)

    print("Business Chat server return code: %s" % r.status_code)


if __name__ == "__main__":
    destination_id = "<source_id from previously received message>"
    send_time_picker_with_user_timezone(destination_id)

# Expected output:
# Business Chat server return code: 200

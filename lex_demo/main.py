#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"


from silvaengine_utility import Utility
from .handlers import handlers_init, validate_handler, fulfillment_handler


# Hook function applied to deployment
def deploy() -> list:
    return [
        {
            "service": "Demo",
            "class": "LexDemo",
            "functions": {
                "booktrip_lex_dispatch": {
                    "is_static": False,
                    "label": "Lex Demo",
                    "query": [],
                    "mutation": [],
                    "type": "RequestResponse",
                    "support_methods": ["POST"],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "beta_core_api",
                    "disabled_in_resources": True,  # Ignore adding to resource list.
                }
            },
        }
    ]


class LexDemo(object):
    def __init__(self, logger, **setting):
        handlers_init(logger, **setting)

        self.logger = logger
        self.setting = setting

    def booktrip_lex_dispatch(self, **kwargs):
        bot = kwargs["bot"]["name"]
        self.logger.info(f"bot: {bot}")

        slots = kwargs["sessionState"]["intent"]["slots"]
        intent = kwargs["sessionState"]["intent"]["name"]
        self.logger.info(f"intent: {intent}")
        self.logger.info(f"slots: {Utility.json_dumps(slots)}")

        if kwargs["invocationSource"] == "FulfillmentCodeHook":
            fulfillment_result = fulfillment_handler(self.logger, intent, slots)
            return {
                "sessionState": {
                    "dialogAction": {"type": "Close"},
                    "intent": {"name": intent, "slots": slots, "state": "Fulfilled"},
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": fulfillment_result["message"],
                    }
                ],
            }

        if kwargs["invocationSource"] == "DialogCodeHook":
            validation_result = validate_handler(self.logger, intent, slots)
            if validation_result["isValid"]:
                return {
                    "sessionState": {
                        "dialogAction": {"type": "Delegate"},
                        "intent": {"name": intent, "slots": slots},
                    }
                }

            if "message" in validation_result:
                return {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result["invalidSlot"],
                            "type": "ElicitSlot",
                        },
                        "intent": {"name": intent, "slots": slots},
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result["message"],
                        }
                    ],
                }

            return {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": validation_result["invalidSlot"],
                        "type": "ElicitSlot",
                    },
                    "intent": {"name": intent, "slots": slots},
                }
            }

#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"


def handlers_init(logger, **setting):
    pass


def validate_handler(logger, intent, slots):
    return {"isValid": True}


def fulfillment_handler(logger, intent, slots):
    return {"message": "I've placed your order."}

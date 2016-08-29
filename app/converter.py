from os.path import dirname, realpath, join
from calendar import timegm
from datetime import datetime
from pygrok import grok_match
from collections import OrderedDict

import json


def convert(message):
    dir_path = dirname(realpath(__file__))
    try:
        log = grok_match(message, '%{LOG}', custom_patterns_dir=join(dir_path, 'patterns'))
    except Exception as e:
        raise Exception('Parsing exception', e) from e
    if not log:
        raise Exception('Message does not match the pattern')
    message = log.pop('message')
    data = OrderedDict([
        ('timestamp', timestamp(log)),
        ('message', message),
    ])
    return encode(data)


def encode(data):
    return json.dumps(data, separators=(',', ':'))


def timestamp(data):
    try:
        time = dict([a, int(x)] for a, x in data.items())
        return timegm(datetime(**time).timetuple())
    except Exception as e:
        raise Exception('Could not build timestamp', e) from e


import os


def get_poll_secs():
    if 'POLL_SECS' in os.environ:
        poll_secs = os.environ['POLL_SECS']
    else:
        poll_secs = 60     # Steve's main requirement

    return poll_secs


def get_telegraf_endpoint():
    if 'TELEGRAF_ENDPOINT' in os.environ:
        telegraf_endpoint = os.environ['TELEGRAF_ENDPOINT']
    else:
        telegraf_endpoint = '192.168.1.180'

    return telegraf_endpoint
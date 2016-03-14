import logging, logging.handlers


def get_logger(name):
    log = logging.Logger(name)
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(levelname)s | %(asctime)-15s - %(module)s::%(funcName)s - %(message)s'))
    log.addHandler(handler)
    return log

import json

def log_debug(logger, data):
    logger.debug(json.dumps(data, indent=2))

def log_error(logger, data):
    logger.error(json.dumps(data, indent=2))

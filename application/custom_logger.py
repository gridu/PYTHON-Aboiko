import logging

logger = logging.getLogger(__name__)
custom_logger = logging.FileHandler('requests.log')
logger.setLevel(logging.INFO)
format_custom_logger = logging.Formatter("%(asctime)s %(message)s")
custom_logger.setFormatter(format_custom_logger)
logger.addHandler(custom_logger)


def loggers(request_type, request_url, center_id, path):

    logger.info('Request type: {0}; URL: {1}; Center id: {2}; Entity type: {3}; Entity id: {4}'
                    .format(request_type, request_url, center_id, path.split("/")[1], path.split("/")[2]))

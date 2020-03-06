import logging

logger = logging.getLogger(__name__)
custom_logger = logging.FileHandler('requests.log')
logger.setLevel(logging.INFO)
format_custom_logger = logging.Formatter("%(asctime)s %(message)s")
custom_logger.setFormatter(format_custom_logger)
logger.addHandler(custom_logger)

center_const = "centers"
register_const = "register"


def log_put_delete_requests(request_type, request_url, center_id, path):
    entity_type = path.split("/")[1]
    entity_id = path.split("/")[2]
    logger.info('Request type: {0}; URL: {1}; Center id: {2}; Entity type: {3}; Entity id: {4}'
                .format(request_type, request_url, center_id, entity_type, entity_id))


def log_post_requests(request_type, request_url, center_id, path):
    entity_type = path.split("/")[1]
    if entity_type == register_const:
        entity_type = center_const
    logger.info('Request type: {0}; URL: {1}; Center id: {2}; Entity type: {3}; Entity id: {4}'
                .format(request_type, request_url, center_id, entity_type, center_id))

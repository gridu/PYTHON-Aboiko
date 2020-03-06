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
    logger.info(
        f'Request type: {request_type};'
        f' URL: {request_url};'
        f' Center id: {center_id};'
        f' Entity type: {entity_type};'
        f' Entity id: {entity_id}')


def log_post_requests(request_type, request_url, center_id, path, generated_id):
    entity_type = path.split("/")[1]
    if entity_type == register_const:
        entity_type = center_const
    logger.info(
        f'Request type: {request_type};'
        f' URL: {request_url};'
        f' Center id: {center_id};'
        f' Entity type: {entity_type};'
        f' Entity id: {generated_id}')

import logging


def logger_maker():
    # Create a logger object

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Check if handlers are already present to avoid adding duplicates

    # Create file handlers for each log file
    http_handler = logging.FileHandler("http_request.log")
    sock_error_handler = logging.FileHandler("sock_error.log")
    # Set the logging level for each handler
    http_handler.setLevel(logging.INFO)
    sock_error_handler.setLevel(logging.INFO)
    # Define the log message format
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    # Assign the format to each handler
    http_handler.setFormatter(formatter)
    sock_error_handler.setFormatter(formatter)
    # Add the handlers to the logger
    logger.addHandler(http_handler)
    logger.addHandler(sock_error_handler)
    return logger


def logger_save(logger, msg, code):
    if code == 1:
        logger.info(msg)
    else:
        logger.error(msg)

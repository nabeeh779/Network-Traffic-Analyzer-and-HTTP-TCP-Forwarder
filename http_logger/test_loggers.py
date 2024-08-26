import logging
from unittest.mock import patch, MagicMock
import pytest
from loggers import logger_save, logger_maker


def test_logger_maker():
    """Test if logger_maker sets up the logger correctly"""
    with patch("logging.FileHandler") as MockFileHandler:
        logger = (
            logger_maker()
        )  # Expected to set up a logger with two file handlers (http_request.log and
        # sock_error.log)

    # Make sure that two files was made
    assert len(logger.handlers) == 2
    # Make sure that the files have correct names
    MockFileHandler.assert_any_call("http_request.log")
    MockFileHandler.assert_any_call("sock_error.log")
    # Ensure that the logging level and formatter are set correctly
    for handler in logger.handlers:
        assert handler.level == logging.INFO
        assert isinstance(handler.formatter, logging.formatter)


@patch.object(logging.Logger, "info")
@patch.object(logging.Logger, "error")
def test_logger_save(mock_error, mock_info):
    """Test logger_save function for both info and error logging"""
    logger = logger_maker()

    # Test info logging
    logger_save(logger, "This is an info message", 1)
    mock_info.assert_called_once_with("This is an info message")
    # Test error logging
    logger_save(logger, "This is an error message", 0)
    mock_error.assert_called_once_with("This is an error message")

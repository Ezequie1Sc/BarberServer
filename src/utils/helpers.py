import logging
from datetime import datetime, date, time

def serialize_datetime(obj):
    """Helper function to serialize datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, time):
        return obj.strftime('%H:%M')
    return obj

def setup_logging(app):
    """Setup logging configuration"""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('api.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
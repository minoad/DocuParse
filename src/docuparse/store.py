import json

from docuparse import config, logger


def save_dict_to_mongo(d: dict, conf: dict[str, str] | None = None) -> bool:
    if not conf:  # conf.get('server', None):
        conf = json.loads('{"test":"test"}')  # config.mongo_db_config)
    logger.info(f"saved {d} to mongodb at {config}.")
    return False


save_dict_to_mongo({})

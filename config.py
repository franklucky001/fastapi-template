import os
from dynaconf import Dynaconf
from typing import List, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import logging
import logging.config
import yaml

settings = Dynaconf(
    warn_dynaconf_global_settings=True,
    environments=True,
    lowercase_read=True,  # case insensitive
    load_dotenv=False,
    settings_files=['conf/settings.toml', 'conf/.secrets.toml']
)


@dataclass_json
@dataclass(frozen=True)
class AppConfig:
    PROJECT_NAME: str
    DEBUG: bool
    VERSION: str
    ALLOWED_HOSTS: List[str]
    PROJECT_DIR: str
    LOG_PATH: str


_all_vars = settings.as_dict()
_all_vars.pop("LOAD_DOTENV", None)
app_config: AppConfig = AppConfig(**_all_vars)


def setup_logging(safety=False):
    config_path = os.path.join(app_config.PROJECT_DIR, "conf/logging.yaml")
    log_path = app_config.LOG_PATH
    if not os.path.exists(log_path):
        print(f"Not Found default log path, create {log_path}")
        os.makedirs(log_path)
    if os.path.exists(config_path):
        if safety:
            from utilities.safe_logging import SafeRotatingFileHandler, SafeTimedRotatingFileHandler
            from logging import handlers
            setattr(handlers, 'SafeRotatingFileHandler', SafeRotatingFileHandler)
            setattr(handlers, 'SafeTimedRotatingFileHandler', SafeTimedRotatingFileHandler)
        with open(config_path, 'r') as f:
            logging_config = yaml.safe_load(f.read())
        origin_handlers = logging_config['handlers']
        for handler_name in origin_handlers:
            if handler_name.startswith('file'):
                handler_file = origin_handlers[handler_name]['filename']
                abs_handler_file = os.path.join(log_path, handler_file)
                origin_handlers[handler_name]['filename'] = abs_handler_file
        logging.config.dictConfig(logging_config)
        print("Init logging by config success !")
    else:
        raise SystemExit(f"logging config file {config_path} not found, exit main processing")


setup_logging(True)
logger = logging.getLogger("project_dummy")

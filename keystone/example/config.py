import json
import os


from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


def _get_config_value(key, default_value=None):
    value = os.environ.get(key, default_value)
    if (value is not None and value != '' and isinstance(value, str)):
        if key.endswith('LIST'):
            value = json.loads(value)

    return value

class BaseConfig(object):
  pass

class DevelopmentConfig(BaseConfig)::
  pass
  
class ProductionConfig(BaseConfig):
  pass

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'staging': StagingConfig,
}

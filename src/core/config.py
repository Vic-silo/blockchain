import os
from dotenv import load_dotenv


class EnvVars:
    BLOCKCHAIN_API_KEY: str
    BLOCKCHAIN_BASE_URL: str

    MONGO_ROOT_USERNAME: str
    MONGO_ROOT_PASSWORD: str
    MONGO_DATABASE: str
    MONGO_URI: str

    LOGS_PATH: str
    DEBUG: str

    def __init__(self, env_file):
        load_dotenv(dotenv_path=env_file)

        # Dynamic load of variables in .env
        for key, value in os.environ.items():
            setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)


# .env file from project base path
env = EnvVars(os.path.join(os.path.dirname(__file__), '..', '.env'))

import logging
from os.path import join
from datetime import datetime
from pathlib import Path
from .config import env

__all__ = [
    "logger",
    "LoggerConfig"
]

class LoggerConfig:
    """
    Class to configure the logger
    """
    _instance = None
    _initialized = False

    __LOG_NAME = 'app-logger'
    __HEAD = '\t'.join(['{asctime}.{msecs:3.0f}', '{levelname:<7}',
                        '{filename}', '{funcName:<20}'])
    __CONSOLE_FORMAT = __HEAD + '\t{message}'
    __FILE_FORMAT = __HEAD + '\t{message}'

    __DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    __FILE_PATH = env.LOGS_PATH
    __FILE_NAME = 'app_log'
    __FILE_NAME_DATE_FORMAT = '%Yy%mm%dd'

    def __new__(cls, name: str = __LOG_NAME):
        """
        Singleton implementation per log name
        """
        if cls._instance is None:
            cls._instance = super(LoggerConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, name: str = __LOG_NAME):
        if not self._initialized:
            # Define the logger
            self.__logger = logging.getLogger(name=name)
            # Define the attributes for the logger
            self.__logger.propagate = False
            self.stream_formatter = self.__formatter(formater_type='console')
            self.logging_level = self.__get_logging_level()
            # Setup the logger handlers
            self.__logger.setLevel(self.logging_level)
            self.__logger.handlers.clear()
            self.__setup_console_handler()
            # Set variable for single initialization
            self._initialized = True
        elif self.__logger.name != name:
            self.__rename_logger(new_name=name)

    def __rename_logger(self, new_name: str) -> None:
        """
        Rename the logger
        :param new_name: New name for the logger
        """
        old_name = self.__logger.name
        self.__logger = logging.getLogger(name=new_name)
        # Transfer the current handlers
        self.__logger.handlers = logging.getLogger(name=old_name).handlers
        # Update properties
        self.__logger.propagate = False
        self.__logger.setLevel(self.logging_level)
        self.__logger.info(f"Logger renamed from {old_name} to {new_name}")

    @property
    def logger(self) -> logging.Logger:
        """
        Get the logger
        :return: The configured logger
        """
        return self.__logger

    @staticmethod
    def __get_logging_level() -> int:
        """
        Get the logging level from the environment variables.
        :return: The logging level
        """
        if env.DEBUG.lower() == 'true':
            return logging.DEBUG
        return logging.INFO

    def __formatter(self, formater_type: str) -> logging.Formatter:
        """
        Create a formatter for the logger.
        :param formater_type: To format the 'console' or 'file' handler
        :return: The formatter
        """
        formatters = {
            'console': self.__CONSOLE_FORMAT,
            'file': self.__FILE_FORMAT
        }
        return logging.Formatter(style='{', fmt=formatters[formater_type],
                                 datefmt=self.__DATE_FORMAT)

    def __setup_console_handler(self) -> None:
        """
        Create a console handler for the logger.
        """
        __console_handler = logging.StreamHandler()
        __console_handler.setLevel(self.logging_level)
        __console_handler.setFormatter(self.stream_formatter)
        self.__logger.addHandler(__console_handler)

    def __setup_file_handler(self, full_path: str) -> None:
        """
        Create a file handler for the logger. It only creates the handler in
        append mode.
        """
        self.__logger.info(msg=f'Logging file set to: {full_path}')
        # Logging file configuration
        __file_handler = logging.FileHandler(filename=full_path)
        __file_handler.setLevel(self.logging_level)
        __file_handler.setFormatter(self.__formatter(formater_type='file'))
        self.__logger.addHandler(__file_handler)

    def add_file_handler(self, filename: str = __FILE_NAME,
                         filepath: str = __FILE_PATH) -> None:
        """
        Create a file handler for the logger.
        :param filename: Name of the output file. The output directory is logs/
        :param filepath: Path to save log. default in /opt/adele
        """
        full_path = self.__build_log_path(filename=filename, filepath=filepath)
        self.__setup_file_handler(full_path=full_path)

    def __build_log_path(self, filename: str, filepath: str) -> str:
        """Build the full log file path."""
        if filename.find('.'):
            filename = filename.split('.')[0]
        log_path = Path(filepath)
        if not log_path.exists():
            log_path.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime(self.__FILE_NAME_DATE_FORMAT)
        filename += f'_{date_str}.log'
        return join(filepath, filename)


# Create default logger to use it directly through the app
_logger_config = LoggerConfig()
logger = _logger_config.logger
_logger_config.add_file_handler()

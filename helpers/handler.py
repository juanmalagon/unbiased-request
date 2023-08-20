from datetime import datetime
from os import environ
from uuid import uuid4
import logging


class Handler:
    @staticmethod
    def get_environment_var(env, fallback):
        try:
            var = environ[env]
            if isinstance(fallback, int):
                var = int(var)
        except (KeyError, ValueError):
            if fallback is None:
                logging.error(
                    f"The required environment variable '{env}' is not set \
                        and has not got a fallback value.")
                raise
            else:
                var = fallback
        return var

    run_date: str = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
    run_serial: str = str(uuid4())

    def __init__(self):

        # Print initialization message
        logging.info('Initializing handler')
        logging.info(f'Run date: {self.run_date}')
        logging.info(f'Run serial: {self.run_serial}')

        # Define environment variables
        self.project_dir = Handler.get_environment_var('project_dir', None)
        self.scopus_config_file = Handler.get_environment_var(
            'scopus_config_file', None)
        self.scopus_data_dir = Handler.get_environment_var(
            'scopus_data_dir', None)
        self.save_to_csv = Handler.get_environment_var('save_to_csv', 0)

        # Collect environment variables
        env_variables_list = {
            'project_dir': self.project_dir,
            'scopus_config_file': self.scopus_config_file,
            'scopus_data_dir': self.scopus_data_dir,
            'save_to_csv': self.save_to_csv
            }

        # Print environment variables
        logging.info('Environment variables:')
        for key, value in env_variables_list.items():
            logging.info(f'{key}: {value}')

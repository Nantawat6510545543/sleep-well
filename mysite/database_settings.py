import logging
import sys

from decouple import config


def configure_database_settings(BASE_DIR):
    """
    Configure database settings for a Django application based on the provided BASE_DIR.

    Args:
        BASE_DIR (Path): The base directory of the Django project.

    Returns:
        dict: A dictionary containing the database settings, including the ENGINE and NAME.
              The specific database settings are determined based on the current environment.

    Note:
        - If running tests (identified by the 'test' argument in sys.argv), the function returns
          settings for the local SQLite database.
        - If a valid user environment variable is found, it configures the database
          using the settings from the user.
        - If user is not found or invalid, it falls back to the local SQLite database.

    """
    local_database = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    testing = sys.argv[1:2] == ['test']
    if testing:
        logging.debug('Running tests on the local database.')
        return local_database

    try:
        user = config("DB_NAME", default=None)
        if user:
            cloud_database = {
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': config("DB_NAME", default=None),
                    'USER': config("DB_USER", default=None),
                    'PASSWORD': config("DB_PASSWD", default=None),
                    'HOST': config("DB_HOST", default=None),
                    'PORT': '',
                }
            }
            logging.info("Using a valid DATABASE_URL. Connecting to the Neon.")
            print("Using a valid DATABASE_URL. Connecting to the Neon.")
            return cloud_database
        else:
            logging.info(
                "DATABASE_URL not found. Falling back to the local database.")
    except ValueError:
        logging.warning(
            "Invalid DATABASE_URL. Falling back to the local database.")

    return local_database

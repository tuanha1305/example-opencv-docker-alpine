import logging
import sys

import toml

from app import App

if __name__ == '__main__':
    # Load configuration
    config = toml.load('config/config.toml')
    if config is None:
        raise Exception('You must configure')

    # Initialize logging
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('').addHandler(console_handler)

    # Log a message indicating that the application has started
    logging.info('Starting the application...')

    # Initialize the Flask app
    app = App(config)

    # Run the Flask app
    app.run()

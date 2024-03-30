import logging
import toml

from app import App

if __name__ == '__main__':
    config = toml.load('config/config.toml')
    if config is None:
        raise Exception('Config is None')
    app = App(config)
    logging.basicConfig(filename='app.log', level=logging.INFO)

    # run app
    app.run()

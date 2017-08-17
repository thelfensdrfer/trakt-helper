import logging
import os

import yaml
from trakt import Trakt

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]: %(message)s'
    )

    # Get the filename of the config file
    config_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'config.yaml'
    )

    # Try to read and parse the config file
    try:
        config = yaml.load(open(config_filename, 'r'))
    except yaml.YAMLError as exc:
        logging.error('Error in configuration file: %', exc)
        exit(1)
    except OSError as exc:
        logging.error('Could not read configuration file: %', exc)

    Trakt.configuration.defaults.client(
        id=config['TRAKT_CLIENT_ID'],
        secret=config['TRAKT_CLIENT_SECRET']
    )

    watched = Trakt['sync/watched'].movies()

    for key, show in watched.shows():
        print(show)
        exit(1)

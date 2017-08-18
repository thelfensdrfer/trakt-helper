import logging
import os

import yaml
import trakt
from trakt.users import User
from terminaltables import AsciiTable

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
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

    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    if 'TRAKT_OAUTH_TOKEN' in config:
        logging.debug('Set oauth token')
        trakt.core.OAUTH_TOKEN = config['TRAKT_OAUTH_TOKEN']
    trakt.init(config['TRAKT_USERNAME'], client_id=config['TRAKT_CLIENT_ID'],
               client_secret=config['TRAKT_CLIENT_SECRET'], store=True)

    user = User(config['TRAKT_USERNAME'])

    # Get all movie ratings
    movie_ratings = user.get_ratings(media_type='movies')

    # Get a list of all watched movies
    movies = user.watched_movies

    # Check which movies were not rated
    unrated_movies = []

    for movie in movies:
        movie_id = movie.ids['ids']['trakt']
        for rating in movie_ratings:
            if movie_id == rating['movie']['ids']['trakt']:
                break
        else:
            unrated_movies.append([
                str(movie.title),
                int(movie.year),
                str('https://trakt.tv/movies/{}'.format(movie.ids['ids']['slug']))
            ])

    # Sort by year and prepend header row
    unrated_movies_sorted = [[
        'Title',
        'Year',
        'Link'
    ]] + sorted(unrated_movies, key=lambda x: x[1])

    # Output unrated movies
    if len(unrated_movies_sorted) > 0:
        print('Unrated Movies:')
        table = AsciiTable(unrated_movies_sorted)
        print(table.table)
    else:
        print('No unrated movies, congratulations!')

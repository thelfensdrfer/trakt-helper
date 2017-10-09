import logging
import os
import argparse

import yaml
import trakt
from trakt.users import User
from terminaltables import AsciiTable


def print_unrated_movies(config):
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
                movie.title,
                movie.year,
                'https://trakt.tv/movies/{}'.format(
                    movie.ids['ids']['slug']
                )
            ])

    # Sort by year and prepend header row
    unrated_movies_sorted = [[
        'Title',
        'Year',
        'Link'
    ]] + sorted(unrated_movies, key=lambda x: x[1])

    # Output unrated movies
    if len(unrated_movies_sorted) > 1:
        print('Unrated Movies:')
        table = AsciiTable(unrated_movies_sorted)
        print(table.table)
    else:
        print('No unrated movies, congratulations!')


def print_unrated_shows(config):
    user = User(config['TRAKT_USERNAME'])

    # Get all movie ratings
    show_ratings = user.get_ratings(media_type='shows')

    # Get a list of all watched shows
    shows = user.watched_shows

    # Check which shows were not rated
    unrated_shows = []

    for show in shows:
        show_id = show.ids['ids']['trakt']
        for rating in show_ratings:
            if show_id == rating['show']['ids']['trakt']:
                break
        else:
            unrated_shows.append([
                show.title,
                show.year,
                'https://trakt.tv/shows/{}'.format(
                    show.ids['ids']['slug']
                )
            ])

    # Sort by year and prepend header row
    unrated_movies_sorted = [[
        'Title',
        'Year',
        'Link'
    ]] + sorted(unrated_shows, key=lambda x: x[1])

    # Output unrated movies
    if len(unrated_movies_sorted) > 1:
        print('Unrated TV Shows:')
        table = AsciiTable(unrated_movies_sorted)
        print(table.table)
    else:
        print('No unrated tv shows, congratulations!')


def print_recommended_movies():
    # Get a list with recommended movies
    movies = [[
        'Title',
        'Year',
        'Link'
    ]] + list(map(lambda movie: [
        movie.title,
        movie.year,
        'https://trakt.tv/movies/{}'.format(
            movie.ids['ids']['slug']
        )], trakt.movies.get_recommended_movies()))

    # Output recommended movies
    if len(movies) > 0:
        print('Recommended movies:')
        table = AsciiTable(movies)
        print(table.table)
    else:
        print('No recommended movies, sorry!')


def print_recommended_shows():
    # Get a list with recommended shows
    shows = [[
        'Title',
        'Year',
        'Link'
    ]] + list(map(lambda movie: [
        movie.title,
        movie.year,
        'https://trakt.tv/shows/{}'.format(
            movie.ids['ids']['slug']
        )], trakt.tv.get_recommended_shows()))

    # Output recommended shows
    if len(shows) > 0:
        print('Recommended tv shows:')
        table = AsciiTable(shows)
        print(table.table)
    else:
        print('No recommended tv shows, sorry!')


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

    # Initialize trakt and authenticate
    trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    if 'TRAKT_OAUTH_TOKEN' in config:
        logging.debug('Set oauth token')
        trakt.core.OAUTH_TOKEN = config['TRAKT_OAUTH_TOKEN']
    trakt.init(config['TRAKT_USERNAME'], client_id=config['TRAKT_CLIENT_ID'],
               client_secret=config['TRAKT_CLIENT_SECRET'], store=True)

    print_unrated_movies(config)
    print_unrated_shows(config)
    print_recommended_movies()
    print_recommended_shows()

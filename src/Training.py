import os
import logging
import sys
from math import sqrt

import pandas as pd
import numpy as np
from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T

        return pred

def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()

    return sqrt(mean_squared_error(prediction, ground_truth))

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

    ratings = pd.read_csv(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'data',
        'ratings.csv'
    ), dtype={
        'userId': np.int32,
        'movieId': np.int32,
        'rating': np.float64,
        'timestamp': np.int64,
    })

    user_count = 138493
    movie_count = 131262

    train_ratings, test_ratings = cv.train_test_split(ratings, test_size=0.25)

    train_data_matrix = np.zeros((user_count, movie_count))
    for index, line in train_ratings.iterrows():
        train_data_matrix[int(line.userId), int(line.movieId)] = int(line.rating * 2)

    test_data_matrix = np.zeros((user_count, movie_count))
    for index, line in test_ratings.iterrows():
        test_data_matrix[int(line.userId), int(line.movieId)] = int(line.rating * 2)

    user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
    user_prediction = predict(train_data_matrix, user_similarity, type='user')

    print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))

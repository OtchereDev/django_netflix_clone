from surprise import SVD, KNNBaseline
from surprise import accuracy
from surprise.model_selection import train_test_split, cross_validate, GridSearchCV
from surprise import Dataset
from surprise import Reader
from surprise.dataset import DatasetAutoFolds

import os
import pandas as pd
import numpy as np

ratings = pd.read_csv('./data/watcha_ratings.csv', encoding = 'utf-8')
movies = pd.read_csv('./data/watcha_movies.csv', encoding = 'utf-8')
users = pd.read_csv('./data/watcha_users.csv', encoding = 'utf-8')

def get_unseen_surprise(ratings, movies, user_index):
    # 입력값으로 들어온 user_index에 해당하는 사용자가 평점을 매긴 모든 영화를 리스트로 생성
    seen_movies = ratings[ratings['user_index'] == user_index]['movie_index'].tolist()
    
    # 모든 영화의 movie_index를 리스트로 생성
    total_movies = movies['movie_index'].tolist()
    
    # 모든 영화의 movie_index를 리스트로 생성
    total_movies = movies['movie_index']
    
    # 모든 영화의 movie_index 중 이미 평점을 매긴 영화의 movie_index를 제외한 후 리스트로 생성
    unseen_movies = [movie for movie in total_movies if movie not in seen_movies]
    print('평점 매긴 영화 수:', len(seen_movies), '추천 대상 영화 수: ', len(unseen_movies),
             '전체 영화 수: ', len(total_movies))
    
    return unseen_movies


def recomm_movie_by_surprise(algo, user_index, unseen_movies, top_n=10):
    
    # 알고리즘 객체의 predict() 메서드를 평점이 없는 영화에 반복 수행한 후 결과를 list 객체로 저장
    predictions = [algo.predict(str(user_index), str(movie_index)) for movie_index in unseen_movies]
    
    def sortkey_est(pred):
        return pred.est
    
    predictions.sort(key = sortkey_est, reverse = True)
    top_predictions = predictions[:top_n]
    
    top_movie_ids = [ int(pred.iid) for pred in top_predictions]
    top_movie_rating = [pred.est for pred in top_predictions]
    top_movie_titles = movies[movies.movie_index.isin(top_movie_ids)]['movie_name']
    
    top_movie_preds = [ (id, title, rating) for id, title, rating in zip(top_movie_ids, top_movie_titles, top_movie_rating)]
    
    return top_movie_preds

def Surprise_KNNBaseline(ratings, movies, users, user_index, n):
    reader = Reader(line_format='user item rating', sep = ',', rating_scale = (0.5, 5))
    data_folds = DatasetAutoFolds(ratings_file='./data/ratings_noh.csv', reader = reader)
    
    # 전체 데이터를 학습 데이터로 생성함
    trainset = data_folds.build_full_trainset()

    algo = KNNBaseline(k=40, min_k=2, sim_options={}, bsl_options={}, verbose=True)
    algo.fit(trainset)

    unseen_movies = get_unseen_surprise(ratings, movies, user_index)

    top_movie_preds = recomm_movie_by_surprise(algo, user_index, unseen_movies, top_n = n)
    
    recomm_df = pd.DataFrame(columns = ['영화 제목', '예상 평점'])
    for i in range(len(top_movie_preds)):
        recomm_df.loc[i,:] = [top_movie_preds[i][1],np.round(top_movie_preds[i][2],2)]
        
        
    return recomm_df
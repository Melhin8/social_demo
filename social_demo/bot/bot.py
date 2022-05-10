#!/usr/bin/env python

import configparser
import random
import requests
# from random import randint, shuffle
import string


def parse_config() -> tuple:
    config = configparser.ConfigParser()
    config.read('config.ini')
    number_of_users = int(config['bot']['number_of_users'])
    max_posts_per_user = int(config['bot']['max_posts_per_user'])
    max_likes_per_user = int(config['bot']['max_likes_per_user'])
    return (number_of_users, max_posts_per_user, max_likes_per_user)


def string_generator(size: int) -> tuple:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def signup_user(user: str) -> tuple:
    username = f"test_{user}"
    password = "Some_Strong_PassWorld"
    email = f"{username}@test.com"
    requests.post(
        f"{url}auth/signup/",
        data={
            'username': username,
            'password': password,
            'email': email
        }
    )
    return (username, password, email)


def get_jwt_token(user: str) -> str:
    r = requests.post(
        f"{url}api/jwt/",
        data={
            'username': f"test_{user}",
            'password': "Some_Strong_PassWorld",
        }
    )
    return r.json()['access']


def post(token: str) -> int:
    r = requests.post(
        f"{url}api/posts/",
        data={
            'title': string_generator(size=16),
            'text': string_generator(size=32),
        },
        headers={
            'Authorization': f"Bearer {token}"
        }
    )
    return r.json()['id']


def like(token: str, post_id: int) -> int:
    r = requests.post(
        f"{url}api/likes/",
        data={
            'post': post_id,
        },
        headers={
            'Authorization': f"Bearer {token}"
        }
    )
    return r.json()['id']


if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/'
    number_of_users, max_posts_per_user, max_likes_per_user = parse_config()
    posts = []
    for _ in range(number_of_users):
        user = string_generator(size=8)
        signup_user(user)
        print(f"User {user} created")
        post_num = random.randint(0, max_posts_per_user)
        print(f"Creating {post_num} posts")
        token = get_jwt_token(user)
        for __ in range(post_num):
            post_id = post(token)
            posts.append(post_id)
            print(f"Post creted with id: {post_id}")
        likes_num = random.randint(0, max_likes_per_user)
        random.shuffle(posts)
        for num in range(likes_num):
            like_id = like(token, posts[num])
            print(f"Like creted with id: {like_id}")

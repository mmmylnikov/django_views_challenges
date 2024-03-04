"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

+ имя пользователя вы узнаёте из урла
+ используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
+ из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
+ если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
+ если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

from django.http import HttpResponse, HttpRequest
import urllib.request
import json
import ssl


def fetch_name_from_github_view(
        request: HttpRequest, github_username: str) -> HttpResponse:

    context = ssl._create_unverified_context()
    try:
        github_response = urllib.request.urlopen(
                f'https://api.github.com/users/{github_username}',
                context=context)
    except urllib.request.HTTPError as err:
        if err.code == 404:
            return HttpResponse('', status=404)

    github_data = json.load(github_response)
    github_name = github_data.get('name', None)
    if github_name:
        github_name = f'"{github_name}"'
    return HttpResponse(f'{{"name": {github_name}}}', status=200)

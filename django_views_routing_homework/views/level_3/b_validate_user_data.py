"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

+ получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
+ если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
+ если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
+ если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
+ есть поле full_name, в нём хранится строка от 5 до 256 символов
+ есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
+ поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
+ других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""
import json

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import (HttpRequest, HttpResponse, HttpResponseBadRequest,
                         JsonResponse)


def validate_full_name(full_name: str) -> None:
    if 5 <= len(full_name) <= 256:
        return
    raise ValidationError('допустимый full_name от 5 до 256 символов')


def validate_existence_fields(
        dictionary: dict,
        required_fields: set[str],
        optional_fields: set[str]) -> None:
    for key in dictionary.keys():
        if key in required_fields:
            required_fields.remove(key)
        elif key in optional_fields:
            optional_fields.remove(key)
        else:
            raise ValidationError(f'"{key}" - невалидное поле')
    if len(required_fields) > 0:
        raise ValidationError(f'не заполнены поля: "{required_fields}"')


def validate_registered_from(
        app: str, choice: tuple[str] = ('website', 'mobile_app')) -> None:
    if app in choice:
        return
    raise ValidationError(f'допустимые "app": "{choice}"')


def validate_age(age: int) -> None:
    if isinstance(age, int):
        return
    raise ValidationError('допустимый "age" - целое число')


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('bad request')

        try:
            validate_existence_fields(
                dictionary=json_data,
                required_fields={'full_name', 'email', 'registered_from'},
                optional_fields={'age'}
            )
            validate_full_name(json_data.get('full_name'))
            validate_email(json_data.get('email'))
            validate_registered_from(json_data.get('registered_from'))
            validate_age(json_data.get('age'))
        except ValidationError:
            return HttpResponse('{"is_valid": false}', status=200)

        return HttpResponse('{"is_valid": true}', status=200)
    return HttpResponse()

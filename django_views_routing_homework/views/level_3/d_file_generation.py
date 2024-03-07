"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

+ ручка должна получать длину генерируемого текста из get-параметра length;
+ дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
+ дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
+ если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

from django.http import HttpRequest, HttpResponse
from faker import Faker


def generate_text(lenght: int | None = None):
    faker = Faker()
    output_text = ''

    if lenght:
        while len(output_text) < lenght:
            output_text += faker.text().replace('\n', ' ')
        output_text = output_text[:lenght]
    else:
        output_text = faker.text().replace('\n', ' ')

    return output_text.strip()


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    max_lenght = 5000
    HttpResponse403 = HttpResponse('', status=403)
    min_length_raw = request.GET.get('length')

    if not min_length_raw:
        return HttpResponse403

    try:
        min_length = int(min_length_raw)
    except ValueError:
        return HttpResponse403

    if min_length > max_lenght or min_length == 0:
        return HttpResponse403

    text_response = HttpResponse(
        generate_text(min_length), status=200, content_type="text/txt",
        headers={"Content-Disposition": 'attachment; filename="text.txt"'},
    )
    return text_response

# -*- coding: utf-8 -*-
from django.db import models
from django.http import HttpResponse
from django.utils import simplejson as json


class JsonDefault(object):
    """ callable class для предоставления произвольного объекта в виде JSON.

    * если объект datetime или date, то вызвать obj.strftime (datetime - это
    подкласс date)
    * если это Decimal, то преобразовать в float, и передать
    * если у объекта есть метод __json__, то возвращает
    obj.__json__()
    """
    def __init__(self, exclude=None, exclude_fk=False):
        self.exclude = exclude or []
        self.exclude_fk = exclude_fk

    def __call__(self, obj):
        import datetime
        from decimal import Decimal
        from django.db.models import Model
        from django.db.models.query import QuerySet
        if isinstance(obj, datetime.date):
            return obj.strftime('%F %T')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, QuerySet):
            return list(obj)
        elif isinstance(obj, models.Manager):
            return list(obj.all())
        elif hasattr(obj, '__json__') and callable(obj.__json__):
            res = obj.__json__()
            # Удаляем ненужные данные
            if isinstance(res, dict):
                if self.exclude_fk:
                    for key, value in res.items():
                        if isinstance(value, QuerySet):
                            del res[key]
                        elif isinstance(value, list):
                            del res[key]
                        elif isinstance(value, Model):
                            del res[key]
                for ex in self.exclude:
                    if ex in res:
                        del res[ex]
            return res
        raise ValueError('%r is not JSON serializable' % obj)


class JSONPWrapper(object):
    """ Класс, который используется для преобразования JSON в JSONP

    Перед преобразованием проверяет два параметра:

    - наличие GET-параметра callback. Если callback не установлен, то
    возвращается обычный json
    - поле referer HTTP-запроса.

    Если всё OK, то возвращается  callback(json)
    """

    callback_key = 'callback'
    accept_www = True

    def __init__(self, request):
        self.request = request
        # parse referer field
        self.referer = request.META.get('HTTP_REFERER', '')
        # parse callback field
        self.callback = request.GET.get(self.callback_key)

    def wrap(self, json_data):
        if self.has_jsonp():
            return '%s(%s)' % (self.callback, json_data)
        return json_data

    def content_type(self):
        return self.has_jsonp() and 'text/javascript' or 'application/json'

    def has_jsonp(self):
        if self.callback is None:  # no need callback
            return False
        return True


def as_json(res, exclude=None, exclude_fk=False, indent=2):
    json_kwargs = dict(
        default=JsonDefault(exclude, exclude_fk), sort_keys=True, indent=indent,
        ensure_ascii=False
    )
    return json.dumps(res, **json_kwargs)


def wrap_json(res, status=None, exclude=None, jsonp_wrapper=None, content_type='application/json'):
    """
    Вернуть объект HttpResponse для указанного объекта.

    В некоторых view передается callback таким образом:
        callback=request.GET.get('callback').

    Это означает, что нужно вернуть не json, а jsonp-объект
    """
    json_res = as_json(res, exclude)
    if jsonp_wrapper:
        content_type = jsonp_wrapper.content_type()
        json_res = jsonp_wrapper.wrap(json_res)
    return HttpResponse(json_res + '\r\n',
        '%s; charset=utf-8' % content_type, status=status)

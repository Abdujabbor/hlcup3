from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .service_factory import ServiceFactory
from django.db import transaction
import json


def account_filter(request):
    return JsonResponse({}, safe=False)


def account_group(request):
    return HttpResponse('Account group endpoint')


def account_recommend(request, id):
    return HttpResponse('Account recommend endpoint: %s' % id)


def account_suggest(request, id):
    return HttpResponse('Account suggest endpoint: %s' % id)


@csrf_exempt
@require_http_methods(['POST'])
def account_create(request):
    body = json.loads(request.body.decode('utf-8'))

    interests = body.pop('interests', [])
    premium = body.pop('premium', [])
    likes = body.pop('likes', [])

    try:
        with transaction.atomic():
            account = ServiceFactory.create_account(body)
            ServiceFactory.add_account_interests(account, interests)
            ServiceFactory.add_account_likes(account, likes)
            ServiceFactory.add_account_subscribe(account, premium)
            return JsonResponse({}, safe=False, status=201)
    except Exception as e:
        print(e)
        return JsonResponse({}, safe=False, status=400)


@csrf_exempt
@require_http_methods(['POST'])
def account_update(request, id):
    body = json.loads(request.body.decode('utf-8'))
    try:
        if ServiceFactory.update_account(id, body) == 0:
            return JsonResponse({}, safe=False, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({}, safe=False, status=400)

    return JsonResponse({}, safe=False, status=202)


@csrf_exempt
@require_http_methods(['POST'])
def account_likes(request):
    body = json.loads(request.body.decode('utf-8'))
    try:
        ServiceFactory.bulk_create_likes(body['likes'])
    except Exception as e:
        print(e)
        return JsonResponse({}, safe=False, status=400)
    return JsonResponse({}, safe=False, status=202)

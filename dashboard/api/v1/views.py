from django.http import JsonResponse


def ping(request):
    data = {"message": "pong!"}
    return JsonResponse(data)

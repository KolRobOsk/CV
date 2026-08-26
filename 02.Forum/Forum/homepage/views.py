from django.http import HttpResponse


def homepage(request):
    return HttpResponse("Witaj na stronie głównej!")

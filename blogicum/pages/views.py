from django.shortcuts import render


def about(request):
    template = 'pages/about.html'
    context = {}
    return render(request, template, context)


def rules(request):
    template = 'pages/rules.html'
    context = {}
    return render(request, template, context)

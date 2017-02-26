from django.shortcuts import render

# Create your views here.
def index(request):
    name = 'HipCityVedge'
    t = 'Favorite'
    context = {'restaurant_name': name,
               'restaurant_type': t }
    return render(request, 'index.html', context)


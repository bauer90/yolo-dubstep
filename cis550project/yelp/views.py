from django.shortcuts import render
from yelp.forms import ZipcodeForm


def index(request):
    return render(request, 'yelp/index.html', [])


def search_zipcode(request):
    if request.method == 'POST':
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            form.save(commit='True')
            print(form)
            return index(request)
        else:
            print(form.errors)
    else:
        form = ZipcodeForm()
    return render(request, 'yelp/search_zipcode.html', {'form': form})


def about(request):
    return render(request, 'yelp/about.html', [])


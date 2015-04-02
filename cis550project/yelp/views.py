from django.shortcuts import render
from yelp.forms import ZipcodeForm
from util import *


def index(request):
    return render(request, 'yelp/index.html', [])


def about(request):
    return render(request, 'yelp/about.html', [])


def search_zipcode(request):
    if request.method == 'POST':
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            form.save(commit='True')
            zipcode_submitted = form.cleaned_data['code']
            return search_zipcode_result(request, zipcode_submitted)
        else:
            print(form.errors)
    else:
        form = ZipcodeForm()
    return render(request, 'yelp/search_zipcode.html', {'form': form})


def search_zipcode_result(request, zipcode):
    result = sql_connect(sql_search_zipcode(zipcode))
    arr = []
    row = result.fetch_row()
    while len(row) > 0:
        arr.append(row[0])
        row = result.fetch_row()
    print(arr)
    return render(request, 'yelp/search_zipcode_result.html', {'zipcode': zipcode,
                                                               'arr': arr,
                                                               })
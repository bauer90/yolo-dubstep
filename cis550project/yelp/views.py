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

    # search nearby businesses
    result = sql_connect(sql_search_zipcode(zipcode))
    arr = []
    row = result.fetch_row()
    while len(row) > 0:
        arr.append(row[0])
        row = result.fetch_row()

    # search nearby zipcodes
    center = sql_connect(sql_zip_center(zipcode)).fetch_row()[0]
    nearby_zipcodes = sql_connect(sql_nearby_zipcodes(float(center[0]), float(center[1]), float(0.1)))
    zipcode_arr = []
    zipcode_row = nearby_zipcodes.fetch_row()
    while len(zipcode_row) > 0:
        if zipcode_row[0] != zipcode:
            zipcode_arr.append(zipcode_row[0])
        zipcode_row = nearby_zipcodes.fetch_row()

    return render(request, 'yelp/search_zipcode_result.html', {'zipcode': zipcode,
                                                               'arr': arr,
                                                               'zipcode_arr': zipcode_arr,
                                                               })

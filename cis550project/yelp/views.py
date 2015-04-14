from django.shortcuts import render
from yelp.forms import ZipcodeForm
from preproc import *
from yelp_api import *


def index(request):
    zipcodes = gen_popular_zipcodes()
    return render(request, 'yelp/index.html', {'zipcodes': zipcodes})


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
    arr = gen_zipcode_result(zipcode)

    # for each business, get an image url
    for i in range(0, len(arr)):
        url = get_business_picture(arr[i][0], arr[i][2] + ", " + arr[i][3])
        arr[i].append(str(url))

    # search nearby zipcodes
    zipcode_arr = gen_zipcodes_nearby(zipcode)

    return render(request, 'yelp/search_zipcode_result.html', {'zipcode': zipcode,
                                                               'arr': arr,
                                                               'zipcode_arr': zipcode_arr,
                                                               })

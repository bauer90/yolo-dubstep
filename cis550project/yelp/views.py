from django.shortcuts import render
from yelp.forms import ZipcodeForm
from preproc import *


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

    # search nearby businesses.
    # after this call, arr has elements that
    # look like [name, stars, city, state]
    arr = gen_zipcode_result(zipcode)

    # for each business, append an image url.
    # after this call, arr has elements that
    # look like [name, stars, city, state, imgurl]
    arr = add_image_to_zipcode_result(arr)

    # for each business, append a bing search result
    # (description of the first search result for that business).
    # after this call, arr has elements that
    # look like [name, stars, city, state, imgurl, bing_des]
    arr = add_bing_to_zipcode_result(arr)

    # search nearby zipcodes
    zipcode_arr = gen_zipcodes_nearby(zipcode)

    return render(request, 'yelp/search_zipcode_result.html', {'zipcode': zipcode,
                                                               'arr': arr,
                                                               'zipcode_arr': zipcode_arr,
                                                               })

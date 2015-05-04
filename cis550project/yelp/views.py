from django.shortcuts import render
from yelp.forms import ZipcodeForm, UserForm, UserProfileForm
from yelp.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from preproc import *


def index(request):
    u = request.user
    location = ''
    if u.is_authenticated():
        profile = UserProfile.objects.get(user=u)  # NOT UserProfile.get() !
        location = getattr(profile, 'location')
        zipcodes = gen_popular_zipcodes_for_state(location)
        auth_flag = True
    else:
        zipcodes = gen_popular_zipcodes()
        auth_flag = False
    return render(request, 'yelp/index.html', {'zipcodes': zipcodes,
                                               'auth_flag': auth_flag,
                                               'location': location,
                                               })


def about(request):
    return render(request, 'yelp/about.html', [])


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            print(profile_form.cleaned_data['location'])
            profile.user = user
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'yelp/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/yelp/')
            else:
                return HttpResponse('Your account is not activated.')
        else:
            return HttpResponse('Invalid login credential.')
    else:
        return render(request, 'yelp/login.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/yelp/')


def current_user_info(request):
    u = request.user
    if u.is_authenticated():
        profile = UserProfile.objects.get(user=u)
        names_and_locs = [
            gen_id_info(profile.desired_1),
            gen_id_info(profile.desired_2),
            gen_id_info(profile.desired_3),
        ]
        tips = [
            gen_tips(profile.desired_1),
            gen_tips(profile.desired_2),
            gen_tips(profile.desired_3),
        ]
        return render(request, 'yelp/current_user.html', {'profile': profile,
                                                          'names_and_locs': names_and_locs,
                                                          'tips': tips,
                                                          })


def add_business(request, business_id):
    u = request.user
    if u.is_authenticated():
        profile = UserProfile.objects.get(user=u)
        print(business_id)
        print('wjefowiehfowiehiowh')
        num = profile.num_businesses_so_far
        if num == 0:
            setattr(profile, 'desired_1', business_id)
            setattr(profile, 'num_businesses_so_far', 1)
            profile.save()

        elif num == 1:
            setattr(profile, 'desired_2', business_id)
            setattr(profile, 'num_businesses_so_far', 2)
            profile.save()
        elif num == 2:
            setattr(profile, 'desired_3', business_id)
            setattr(profile, 'num_businesses_so_far', 3)
            profile.save()
        else:
            return render(request, 'yelp/index.html', {})
        return render(request, 'yelp/current_user.html', {'profile': profile})
    else:
        return render(request, 'yelp/index.html', {})


def search_zipcode(request):
    if request.method == 'POST':
        form = ZipcodeForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['cat'])
            form.save(commit='True')
            zipcode_submitted = form.cleaned_data['code']
            category_submitted = form.cleaned_data['cat']
            return search_zipcode_result(request, zipcode_submitted, category_submitted)
        else:
            print(form.errors)
    else:
        form = ZipcodeForm()
    return render(request, 'yelp/search_zipcode.html', {'form': form})


def search_zipcode_result(request, zipcode, category):

    # search nearby businesses.
    # after this call, arr has elements that
    # look like [name, stars, city, state]
    arr = gen_zipcode_result(zipcode, category)
    zipcode_arr = []

    if arr:
        # for each business, append an image url.
        # after this call, arr has elements that
        # look like [name, stars, city, state, imgurl]
        arr = add_image_to_zipcode_result(arr)
        print arr
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
                                                               'cat': category
                                                               })


# Philadelphia as default location (40,-75)
def google_map(request, name_and_locs):
    return render(request, 'yelp/google_map_direction.html', {'name_and_locs', name_and_locs,
                                                              })
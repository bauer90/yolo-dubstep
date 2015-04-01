from django.shortcuts import render
from yelp.forms import ZipcodeForm
import _mysql


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
    conn = _mysql.connect('mysql.cb0rrjncuorj.us-west-2.rds.amazonaws.com',
                          'erhan',
                          '550300321',
                          'mydb')
    conn.query("""select b.name, b.state
                  from BUSINESS as b
                  where b.zipcode = '""" + zipcode + "' limit 25")
    result = conn.use_result()
    arr = []
    row = result.fetch_row()
    while len(row) > 0:
        arr.append(row[0])
        row = result.fetch_row()
    conn.close()
    print(arr)
    return render(request, 'yelp/search_zipcode_result.html', {'zipcode': zipcode,
                                                               'arr': arr,
                                                               })
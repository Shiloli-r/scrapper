from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

# https://losangeles.craigslist.org/search/bbb?query=python+tutor&sort=rel&lang=en&cc=gb
# BASE_URL = 'https://losangeles.craigslist.org/search/bbb?query={}'
BASE_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craiglist.org/{}_300x300.jpg'



# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    url = BASE_URL.format(quote_plus(search))  # joins the base url to the user search
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('li', {'class': 'result-row'})

    postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]  # gets img id
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_id, post_image_url)
        else:
            post_image_url = "https://craiglist.org/images/peace.jpg"
            # https://losangeles.craigslist.org/images/peace.jpg

        postings.append((post_title, post_url, post_price, post_image_url))  # append a tuple to the postings list

    send_to_frontend = {
        'search': search,
        'postings': postings,
    }
    return render(request, 'scrap/new_search.html', context=send_to_frontend)

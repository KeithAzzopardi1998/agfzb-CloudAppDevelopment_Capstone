from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)




# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    #context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
    
    return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://b591b18d.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context = {'dealerships' : dealerships}
        print("dealerships context:")
        print(dealerships)
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://b591b18d.us-south.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealer_id=dealer_id)
        # Concat all dealer's short name
        review_vals = ' '.join(["%s (%s)"%(r.review,r.sentiment) for r in reviews])
        # Return a context with the dealer info
        context = { 
            'reviews': reviews,
            'dealer_id': dealer_id
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    #context = {}
    # Handles GET request
    if request.method == "GET":
        context = {
            'dealer_id' : dealer_id,
            'cars' : []
        }
        return render(request, 'djangoapp/add_review.html', context)

    # Handles POST request
    if request.method == "POST":
        # check if user is authenticated
        if request.user.is_authenticated:
            # If user is valid, we can post the review
            review = {
                "name": "Test User X",
                "dealership": dealer_id,
                "review": "good serivce, people were very helpful",
                "purchase": True,
                "purchase_date": "03/18/2021",
                "car_make": "Audi",
                "car_model": "Q2",
                "car_year": 2019
            }
            json_payload = { "review" : review}
            url = "https://b591b18d.us-south.apigw.appdomain.cloud/api/review"
            response = post_request(url=url,json_payload=json_payload)
            return HttpResponse(response)
        else:
            print("authentication failed")
            return HttpResponse("Please log in")


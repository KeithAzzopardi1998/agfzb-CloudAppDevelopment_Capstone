import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url,api_key=None,params={}):
    print(params)
    print("GET from {} ".format(url))
    try:
        if api_key:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=params)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return {'code': status_code, 'json': json_data}

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, params={}):
    print(params)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=params, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return {'code': status_code, 'json': json_data}    

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)['json']
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    params = { 'state' : state}
    json_result = get_request(url,params=params)['json']
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer_doc in dealers:
            # Get its content in `doc` object
            #dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
    
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    params = {'dealerId': dealer_id}
    json_result = get_request(url,params=params)['json']
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["entries"]
        # For each dealer object
        for review_doc in reviews:
            # Create a CarDealer object with values in `doc` object
            if bool(review_doc['purchase']):
                rev_obj = DealerReview(dealership=review_doc['dealership'], 
                                        name=review_doc['name'],
                                        purchase=review_doc['purchase'], 
                                        review=review_doc['review'],
                                        purchase_date=review_doc['purchase_date'],
                                        #purchase_year=review_doc['purchase_date'][-4:],
                                        car_make=review_doc['car_make'],
                                        car_model=review_doc['car_model'],
                                        car_year=review_doc['car_year'],
                                        #sentiment=review_doc['sentiment'],
                                        sentiment=analyze_review_sentiments(review_doc['review']),
                                        id=review_doc['id'])
            else:
                rev_obj = DealerReview(dealership=review_doc['dealership'], 
                                        name=review_doc['name'],
                                        purchase=review_doc['purchase'], 
                                        review=review_doc['review'],
                                        #sentiment=review_doc['sentiment'],
                                        sentiment=analyze_review_sentiments(review_doc['review']),
                                        id=review_doc['id'])                
            results.append(rev_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    params = {
        'text': text,
        'version': '2021-03-25',
        'features': ['sentiment'],
        'return_analyzed_text': 'true',
    }
    api_key = '8pwUxAjLPw_LuzT0XKgRCaIvaFB8fOCTbg-B8tL7jte8'
    #url = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/d93cc945-5317-4497-aa7b-26b616c6130d'
    url = 'https://gateway.watsonplatform.net/natural-language-understanding/api/v1/analyze'
    response = get_request(url=url,api_key=api_key,params=params)
    if response['code'] == 200:
        return response['json']['sentiment']['document']['label']
    elif response['code'] == 422:
        #text too short to analyze, return neutral
        return "neutral"
    else:
        return "failure"



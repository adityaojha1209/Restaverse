from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
import requests
from allauth.socialaccount.models import SocialToken
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

mockReviews = {
    "reviews": [
    {
      "reviewId": "123456789",
      "reviewer": {
        "displayName": "John Doe",
        "profilePhotoUrl": "https://example.com/photo.jpg",
        "isAnonymous": False
      },
      "comment": "Great service and friendly staff! Highly recommend.",
      "starRating": "FIVE",
      "createTime": "2024-12-21T10:00:00Z",
      "updateTime": "2024-12-21T12:00:00Z",
      "reviewReply": {
        "comment": "Thank you, John! We’re glad you had a great experience.",
        "updateTime": "2024-12-21T14:00:00Z"
      }
    },
    {
      "reviewId": "987654321",
      "reviewer": {
        "displayName": "Jane Smith",
        "profilePhotoUrl": "https://example.com/photo2.jpg",
        "isAnonymous": False
      },
      "comment": "The bread was stale and overpriced. Disappointed.",
      "starRating": "TWO",
      "createTime": "2024-12-20T08:30:00Z",
      "updateTime": "2024-12-20T09:00:00Z",
      "reviewReply": {
        "comment": "We’re sorry for your experience, Jane. Please contact us to resolve this issue.",
        "updateTime": "2024-12-20T10:00:00Z"
      }
    },
    {
      "reviewId": "567890123",
      "reviewer": {
        "displayName": "Anonymous",
        "profilePhotoUrl": "",
        "isAnonymous": True
      },
      "comment": "Amazing ambiance and delicious pastries.",
      "starRating": "FOUR",
      "createTime": "2024-12-18T15:20:00Z",
      "updateTime": "2024-12-18T15:20:00Z",
      "reviewReply": ""
    },
    {
      "reviewId": "112233445",
      "reviewer": {
        "displayName": "Michael Johnson",
        "profilePhotoUrl": "https://example.com/photo3.jpg",
        "isAnonymous": False
      },
      "comment": "Very cozy place and the cakes are fantastic! I’ll be back.",
      "starRating": "FIVE",
      "createTime": "2024-12-17T18:45:00Z",
      "updateTime": "2024-12-17T19:00:00Z",
      "reviewReply": {
        "comment": "Thanks for your feedback, Michael! We look forward to seeing you again soon.",
        "updateTime": "2024-12-17T20:00:00Z"
      }
    },
    {
      "reviewId": "334455667",
      "reviewer": {
        "displayName": "Emily White",
        "profilePhotoUrl": "https://example.com/photo4.jpg",
        "isAnonymous": False
      },
      "comment": "The staff was friendly, but the coffee was too weak for my taste.",
      "starRating": "THREE",
      "createTime": "2024-12-16T10:10:00Z",
      "updateTime": "2024-12-16T11:00:00Z",
      "reviewReply": {
        "comment": "We appreciate your feedback, Emily. We’ll look into improving the coffee strength.",
        "updateTime": "2024-12-16T12:00:00Z"
      }
    },
    {
      "reviewId": "998877665",
      "reviewer": {
        "displayName": "Sophia Green",
        "profilePhotoUrl": "https://example.com/photo5.jpg",
        "isAnonymous": False
      },
      "comment": "Wonderful gluten-free options, loved the chocolate croissants!",
      "starRating": "FIVE",
      "createTime": "2024-12-15T09:30:00Z",
      "updateTime": "2024-12-15T10:00:00Z",
      "reviewReply": {
        "comment": "Thank you, Sophia! We’re so glad you enjoyed our gluten-free treats.",
        "updateTime": "2024-12-15T10:30:00Z"
      }
    },
    {
      "reviewId": "556677889",
      "reviewer": {
        "displayName": "Liam Brown",
        "profilePhotoUrl": "https://example.com/photo6.jpg",
        "isAnonymous": False
      },
      "comment": "Nice place, but the pastries are a bit too sweet for my liking.",
      "starRating": "THREE",
      "createTime": "2024-12-14T14:40:00Z",
      "updateTime": "2024-12-14T15:00:00Z",
      "reviewReply": {
        "comment": "Thanks for sharing your opinion, Liam! We will consider offering less sweet options in the future.",
        "updateTime": "2024-12-14T16:00:00Z"
      }
    }
  ]
}

@api_view(['GET'])
def get_reviews(request):
    return JsonResponse(mockReviews, safe=False)

# def logout(request):
#   logout(request)

'''def login(request):
  google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
  client_id = "255102167652-f47m1u1p8opljejslqssdcg4qndc572o.apps.googleusercontent.com"
  redirect_uri = "http://localhost:3000/api/auth/callback"  
  scope = "openid email profile"
  response_type = "code"

  # Construct the Google login URL
  google_login_url = (
      f"{google_auth_url}?client_id={client_id}"
      f"&redirect_uri={redirect_uri}"
      f"&response_type={response_type}&scope={scope}"
  )

  return JsonResponse({"url": google_login_url})


def get_google_access_token(user):
    token = SocialToken.objects.filter(account__user=user, account__provider='google').first()
    if token:
        return token.token
    return None


def fetch_business_reviews(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    # Get accountId
    accounts_url = 'https://mybusinessbusinessinformation.googleapis.com/v1/accounts'
    accounts_response = requests.get(accounts_url, headers=headers)
    accounts_data = accounts_response.json()
    account_id = accounts_data['accounts'][0]['name'].split('/')[-1]

    # Get locationId and reviews
    locations_url = f'https://mybusinessbusinessinformation.googleapis.com/v1/accounts/{account_id}/locations'
    locations_response = requests.get(locations_url, headers=headers)
    locations_data = locations_response.json()

    reviews = []
    for location in locations_data['locations']:
        location_id = location['name'].split('/')[-1]
        reviews_url = f'https://mybusinessbusinessinformation.googleapis.com/v1/accounts/{account_id}/locations/{location_id}/reviews'
        reviews_response = requests.get(reviews_url, headers=headers)
        reviews_data = reviews_response.json()
        reviews.extend(reviews_data.get('reviews', []))

    return reviews

@login_required
def fetch_reviews_view(request):
    access_token = get_google_access_token(request.user)
    if access_token:
        reviews = fetch_business_reviews(access_token)
        return render(request, 'reviews.html', {'reviews': reviews})
    return render(request, 'error.html', {'message': 'Unable to fetch reviews'})'''


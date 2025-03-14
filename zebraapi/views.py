from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ZebraQuery, ZebraResult
from .serializers import ZebraQuerySerializer
import requests
from bs4 import BeautifulSoup
import tweepy
from instaloader import Instaloader, Profile
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Special Zebra API!")

class SpecialZebraViewSet(viewsets.ModelViewSet):
    queryset = ZebraQuery.objects.all()
    serializer_class = ZebraQuerySerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            query = serializer.save()
            self.fetch_data(query)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def fetch_data(self, query):
        input_value = query.input_value
        input_type = query.input_type

        url = f"https://www.google.com/search?q={input_value}+Kenya"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('a[href]')[:5]]
        ZebraResult.objects.create(query=query, source='Web', data={'links': links})

        try:
            auth = tweepy.OAuthHandler("your_api_key", "your_api_secret")  
            api = tweepy.API(auth)
            user = api.get_user(screen_name=input_value.lstrip('@'))
            data = {
                'username': user.screen_name,
                'followers': user.followers_count,
                'bio': user.description,
                'pic_url': user.profile_image_url_https
            }
            ZebraResult.objects.create(query=query, source='Twitter', data=data)
        except Exception as e:
            ZebraResult.objects.create(query=query, source='Twitter', data={'error': str(e)})

        # Ig(stubbed - public profiles only)
        loader = Instaloader()
        try:
            profile = Profile.from_username(loader.context, input_value.lstrip('@'))
            data = {
                'username': profile.username,
                'followers': profile.followers,
                'bio': profile.biography,
                'pic_url': profile.profile_pic_url
            }
            ZebraResult.objects.create(query=query, source='Instagram', data=data)
        except Exception as e:
            ZebraResult.objects.create(query=query, source='Instagram', data={'error': str(e)})
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ZebraQuery, ZebraResult
from .serializers import ZebraQuerySerializer
import requests
from bs4 import BeautifulSoup
import tweepy
from instaloader import Instaloader, Profile

class SpecialZebraViewSet(viewsets.ModelViewSet):
    queryset = ZebraQuery.objects.all()
    serializer_class = ZebraQuerySerializer
    # permission_classes = [IsAuthenticated]  # Uncomment for auth

    def perform_create(self, serializer):
        query = serializer.save()
        self.fetch_data(query)

    def fetch_data(self, query):
        input_value = query.input_value
        input_type = query.input_type

        url = f"https://www.google.com/search?q={input_value}+Kenya"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.select('a[href^=http]') if 'google.com' not in a['href']][:5]
        ZebraResult.objects.create(query=query, source='Web', data={'links': links if links else ['No relevant links found']})

        try:
            auth = tweepy.OAuthHandler("your_actual_api_key", "your_actual_api_secret")
            auth.set_access_token("your_access_token", "your_access_token_secret")  
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
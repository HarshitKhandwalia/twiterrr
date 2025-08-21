from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponse, Http404
from django.conf import settings
import os

def index(request):
  return render(request,'index.html')

def test_view(request):
    """Simple test view to debug 400 errors"""
    return HttpResponse("Test view working! Request method: " + request.method)

def serve_media(request, path):
    """Custom view to serve media files in production"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read())
            # Set content type based on file extension
            if path.endswith('.jpg') or path.endswith('.jpeg'):
                response['Content-Type'] = 'image/jpeg'
            elif path.endswith('.png'):
                response['Content-Type'] = 'image/png'
            elif path.endswith('.gif'):
                response['Content-Type'] = 'image/gif'
            else:
                response['Content-Type'] = 'application/octet-stream'
            return response
    else:
        raise Http404("File not found")

def tweet_list(request):
  tweets = Tweet.objects.all().order_by('-created_at')
  # Debug: print photo information
  for tweet in tweets:
      if tweet.photo:
          print(f"DEBUG: Tweet {tweet.id} has photo: {tweet.photo}")
          print(f"DEBUG: Photo path: {tweet.photo.path}")
          print(f"DEBUG: Photo URL: {tweet.photo.url}")
          print(f"DEBUG: Photo exists: {os.path.exists(tweet.photo.path)}")
  return render(request, 'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
  if request.method == "POST":
    form = TweetForm(request.POST, request.FILES)
    if form.is_valid():
     tweet = form.save(commit=False)
     tweet.user = request.user
     tweet.save()
     print(f"DEBUG: Tweet created with photo: {tweet.photo}")  # Debug line
     print(f"DEBUG: Photo URL: {tweet.photo.url if tweet.photo else 'No photo'}")  # Debug line
     return redirect('tweet_list')
  else:
    form = TweetForm()
  return render(request,'tweetform.html',{'form':form})    

@login_required
def tweet_edit(request,tweet_id):
  tweet = get_object_or_404(Tweet,pk = tweet_id,user = request.user)
  if request.method == 'POST':
    form = TweetForm(request.POST,request.FILES,instance=tweet)
    if form.is_valid():
      tweet = form.save(commit=False)
      tweet.user = request.user
      tweet.save()
      return redirect('tweet_list')
  else:
    form = TweetForm(instance=tweet)
  return render(request, 'tweetform.html',{'form':form})  

@login_required
def tweet_del(request, tweet_id):
  tweet = get_object_or_404(Tweet,pk = tweet_id, user =request.user )
  if request.method == "POST":
    tweet.delete()
    return redirect('tweet_list')
  return render(request, 'tweet_confirm_del.html',{'tweet':tweet})  


def register(request):
    if request.method == "POST":
      form = UserRegistrationForm(request.POST)
      if form.is_valid():
        user = form.save(commit=False);
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request,user)
        return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})    


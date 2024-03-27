from django.shortcuts import render
from django.http import HttpResponse, Http404
from .forms import Signup, Login, EditForm
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Song, Playlist

# Create your views here.
my_playlists = [
    {"id": 1, "name": "Car Playlist", "numberOfSongs": 4},
    {"id": 2, "name": "Coding Playlist", "numberOfSongs": 2},
]

my_songs = [
    {
        "id": 1,
        "Track": "thank u, next",
        "Artist": "Ariana Grande",
        "Album": "thank u, next",
        "Length": "3:27",
        "playlist_id": 1,
    },
    {
        "id": 2,
        "Track": "One Kiss, next",
        "Artist": "Dua Lipa, Calvin Harris",
        "Album": "One Kiss",
        "Length": "3:34",
        "playlist_id": 1,
    },
    {
        "id": 3,
        "Track": "Better Now",
        "Artist": "Post Malone",
        "Album": "beerbongs & bentleys",
        "Length": "3:51",
        "playlist_id": 1,
    },
    {
        "id": 4,
        "Track": "The Middle",
        "Artist": "Grey,Marren Morris, ZEDD",
        "Album": "The Middle",
        "Length": "3:04",
        "playlist_id": 1,
    },
    {
        "id": 5,
        "Track": "Love Lies",
        "Artist": "Normani, Khalid",
        "Album": "Love Lies",
        "Length": "3:21",
        "playlist_id": 2,
    },
    {
        "id": 6,
        "Track": "Rise",
        "Artist": "Jack & Jack, Jonas Blue",
        "Album": "Blue",
        "Length": "3:14",
        "playlist_id": 2,
    },
]

users = [
    {
        "id": 1,
        "full_name": "john",
        "email": "john123@gmail.com",
        "password": "adminpass",
    },
]


def about(request):
    try:
        for playlist in my_playlists:
            play_list = Playlist(
                id=playlist["id"],
                name=playlist["name"],
                numberOfSongs=playlist["numberOfSongs"],
            )
            play_list.save()

        for song in my_songs:
            song_to_add = Song(
                id=song["id"],
                track=song["Track"],
                artist=song["Artist"],
                album=song["Album"],
                length=song["Length"],
            )
            song_to_add.save()
            song_to_add.playlist.add(
                Playlist.objects.get(id=song["playlist_id"]))

    except Exception as e:
        print(e)
    return HttpResponse(
        """<h1>About Us:</h1><p>With Zing, you can easily find the music of your choice and easily share it with other people. You can also browse through the collections of friends, artists, and celebrities, or create a playlist of your own.
      Soundtrack your life with Zing. Subscribe or listen for free.</p>"""
    )


def edit_song(request, song_id):
    song = Song.objects.get(id=song_id)

    inital_form_data = {
        "track": song.track,
        "album": song.album,
        "artist": song.artist,
        "length": song.length,
    }

    form = EditForm(request.POST or None, initial=inital_form_data)

    if form.is_valid():
        cd = form.cleaned_data
        print(cd)

        song.track = cd["track"]
        song.album = cd["album"]
        song.artist = cd["artist"]
        song.length = cd["length"]
        song.save()

        song.playlist.add(cd["playlist"][0])

        return render(
            request,
            "zing_it/edit.html",
            {"form": form, "status": "Your song is updated successfully!"},
        )

    return render(request, "zing_it/edit.html", {"form": form})


def playlists(request, playlist_id):
    songs = []
    playlist_name = ""
    playlist_data = Playlist.objects.get(pk=playlist_id)

    playlist_name = playlist_data.name

    """ for playlist in playlist_data:
        if playlist_id == playlist['id']:
            playlist_name = playlist['name'] """

    if len(playlist_name) == 0:
        raise Http404("Such playlist does not exist")

    song_data = Song.objects.filter(playlist__id=playlist_id)
    for song in song_data:
        songs.append(song)

    return render(
        request, "zing_it/songs.html", {"songs": songs,
                                        "playlist_name": playlist_name}
    )


def home(request):
    user_playlists = Playlist.objects.all()
    return render(request, "zing_it/home.html", {"my_playlists": user_playlists})


def sign_up(request):
    form = Signup(request.POST or None)
    status = ""
    if form.is_valid():
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        email = form.cleaned_data.get("email")
        fullname = form.cleaned_data.get("fullname")
        if password != confirm_password:
            status = "Your passwords do not match"
            return render(
                request, "zing_it/signup.html", {
                    "form": form, "status": status}
            )

        try:
            user = User.objects.get(email=email)
            status = "This email already exists in the system! Please login instead"
            return render(
                request, "zing_it/signup.html", {
                    "form": form, "status": status}
            )
        except Exception as e:
            print(e)
            user = User.objects.create_user(fullname, email, password)
            user.save()
            status = "Sign up successful"
    return render(request, "zing_it/signup.html", {"form": form, "status": status})


def login(request):
    form = Login(request.POST or None)
    status = ""
    if form.is_valid():
        cd = form.cleaned_data

        user = auth.authenticate(
            username=cd["username"], password=cd["password"])
        if user:
            auth.login(request, user)
            status = "Login successful"
        else:
            status = "Invalid credentials"
    return render(request, "zing_it/login.html", {"form": form, "status": status})

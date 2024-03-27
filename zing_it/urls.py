from django.urls import path
from . import views


app_name = "songs"
urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("playlist/<int:playlist_id>", views.playlists, name="playlist"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("login/", views.login, name="login"),
    path("edit/<int:song_id>", views.edit_song, name="edit_song"),
]

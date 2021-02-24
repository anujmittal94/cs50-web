from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed", views.closed, name="closed"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/startwatch", views.startwatch, name="startwatch"),
    path("listing/<int:listing_id>/stopwatch", views.stopwatch, name="stopwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("listing/<int:listing_id>/open", views.open, name="open"),
    path("listing/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watch
from .forms import NewListingForm, NewBidForm, NewCommentForm

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(open_status = True).order_by('-id')
    })

def closed(request):
    return render(request, "auctions/closed.html", {
        "listings": Listing.objects.filter(open_status = False).order_by('-id')
    })

def categories(request):
    category_name = False
    return render(request, "auctions/categories.html", {
        "categories": Listing.categories,
        "category_name": category_name
    })

def category(request, category):
    category_name = "Category Not Found"
    for categoryl, category_namel in Listing.categories:
        if categoryl == category:
            category_name = category_namel
    return render(request, "auctions/categories.html", {
        "listings": Listing.objects.filter(category = category).order_by('-id'),
        "category_name": category_name
    })

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        createform = NewListingForm(request.POST)
        new_listing = createform.save(commit = False)
        new_listing.lister = request.user
        new_listing.save()
        new_watch = Watch(watcher = request.user, listing = new_listing)
        new_watch.save()
        messages.success(request, f"Successfully listed {new_listing.title} and added to Watchlist")
        return render(request, "auctions/create.html", {
            "createform": NewListingForm()
        })
    else:
        return render(request, "auctions/create.html", {
            "createform": NewListingForm()
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk = listing_id)
    if len(listing.bidsonlisting.all()) != 0:
        current_bid = listing.bidsonlisting.all().latest('amount')
    else:
        current_bid = False
    if request.user.is_authenticated:
        if len(listing.userswatching.filter(watcher = request.user)) == 0:
            userwatching = False
        else:
            userwatching = True
    else:
        userwatching = False
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bidform": NewBidForm(),
        "commentform": NewCommentForm(),
        "bids": listing.bidsonlisting.filter().order_by('-id')[:5],
        "current_bid": current_bid,
        "comments": listing.commentsonlisting.all(),
        "userwatching": userwatching
    })


@login_required(login_url='login')
def startwatch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if len(listing.userswatching.filter(watcher = request.user)) == 0:
            new_watch = Watch(watcher = request.user, listing = listing)
            new_watch.save()
            messages.success(request, f"Listing added to Watchlist")
        else:
            messages.error(request, f" Listing already in Watchlist")
        return redirect("listing", listing_id)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def stopwatch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if len(listing.userswatching.filter(watcher = request.user)) != 0:
            listing.userswatching.filter(watcher = request.user).delete()
            messages.success(request, f"Listing removed from watchlist")
        else:
            messages.error(request, f"Listing not in watchlist")
        return redirect("listing", listing_id)
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watched": request.user.userwatchlist.all().order_by('-id')
    })

@login_required(login_url='login')
def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if request.user == listing.lister:
            listing.open_status = False
            listing.save()
            return redirect("listing", listing_id)
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def open(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        if request.user == listing.lister:
            listing.open_status = True
            listing.save()
            return redirect("listing", listing_id)
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        old_price = listing.current_price
        bidform = NewBidForm(request.POST)
        new_bid = bidform.save(commit = False)
        new_bid.bidder = request.user
        new_bid.listing = listing
        listing.current_price = new_bid.amount
        if len(listing.bidsonlisting.all()) == 0 and old_price <= new_bid.amount:
            new_bid.save()
            listing.save()
            messages.success(request, f"Made bid of ${new_bid.amount} (Recommendation: Add to your Watchlist)")
        elif old_price < new_bid.amount:
            new_bid.save()
            listing.save()
            messages.success(request, f"Made  bid of ${new_bid.amount} (Recommendation: Add to your Watchlist)")
        else:
            messages.error(request, f"Bid of ${new_bid.amount} was was too small.")
        return redirect("listing", listing_id)
    else:
        return HttpResponseRedirect(reverse("index"))


def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        commentform = NewCommentForm(request.POST)
        new_comment = commentform.save(commit = False)
        new_comment.commenter = request.user
        new_comment.listing = listing
        new_comment.save()
        messages.success(request, f"Comment Added")
        return redirect("listing", listing_id)
    else:
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

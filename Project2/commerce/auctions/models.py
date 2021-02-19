from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listingsbyuser")
    title = models.CharField(max_length = 200)
    description = models.TextField(max_length = 500)
    current_price = models.DecimalField(max_digits = 11,decimal_places = 2)
    image_url = models.URLField(blank = True)
    categories = [
        ("AM", "Art & Music"),
        ("BI", "Biographies"),
        ("BU", "Business"),
        ("CO", "Comics"),
        ("CT", "Computers & Tech"),
        ("CK", "Cooking"),
        ("ER", "Education & Reference"),
        ("EN", "Entertainment"),
        ("LQ", "LGBTQ"),
        ("HF", "Health & Fitness"),
        ("HI", "History"),
        ("HC", "Hobbies & Crafts"),
        ("HG", "Home & Garden"),
        ("HO", "Horror"),
        ("KI", "Kids"),
        ("LF", "Literature & Fiction"),
        ("ME", "Medical"),
        ("MY", "Mysteries"),
        ("PA", "Parenting"),
        ("RE", "Religion"),
        ("RO", "Romance"),
        ("SF", "Sci-Fi & Fantasy"),
        ("SM", "Science & Math"),
        ("SH", "Self-Help"),
        ("SS", "Social Sciences"),
        ("SP", "Sports"),
        ("TE", "Teen"),
        ("TR", "Travel"),
        ("TC", "True Crime"),
        ("UM", "Uncategorized & Misc"),
        ("WE", "Westerns"),

    ]
    category = models.CharField(max_length = 2, choices = categories, default = "UM")
    open_status = models.BooleanField(default = True)

    def __str__(self):
        return f"Listing {self.id} by {self.lister}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidsbyuser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidsonlisting")
    amount = models.DecimalField(max_digits = 11, decimal_places = 2)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentsbyuser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentsonlisting")
    comment = models.TextField(max_length = 500)

class Watch(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userwatchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="userswatching")

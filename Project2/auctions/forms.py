from django import forms
from django.forms import TextInput, URLInput, Textarea, NumberInput, Select
from .models import Listing, Bid, Comment

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "image_url", "description", "current_price", "category"]
        labels = {
            "title": "Item Name",
            "image_url": "Image URL (Please enter the full URL or leave blank for no image)",
            "description": "Item Description",
            "current_price": "Starting Price",
            "category": "Category (If more than one fits, choose the most prominent!)"
        }
        widgets = {
            "title": TextInput(attrs={"class":"form-control"}),
            "image_url": URLInput(attrs={"class":"form-control"}),
            "description": Textarea(attrs={"class":"form-control"}),
            "current_price": NumberInput(attrs={"class":"form-control", "max": "999999999.99"}),
            "category": Select(attrs={"class":"form-control"})
        }

class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": NumberInput(attrs={"class":"form-control"})
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": Textarea(attrs={"class":"form-control"})
        }

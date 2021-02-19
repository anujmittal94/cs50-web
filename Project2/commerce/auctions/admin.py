from django.contrib import admin
from .models import User, Listing, Bid, Comment, Watch

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "lister", "title", "current_price")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bidder", "listing", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "commenter")

class WatchAdmin(admin.ModelAdmin):
    list_display = ("id", "watcher", "listing")
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watch, WatchAdmin)

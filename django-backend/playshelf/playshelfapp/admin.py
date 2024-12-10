from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(GamePlatform)
admin.site.register(Genre)
admin.site.register(GameGenre)
admin.site.register(Wishlist)
admin.site.register(GameImage)
admin.site.register(Developer)
admin.site.register(Review)
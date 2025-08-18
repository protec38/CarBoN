import os

import django

django.setup()

from django.contrib.auth.models import User

if len(User.objects.all()) == 0:
    print("No users: this is a new installation. Creating a super user.")
    admin = User.objects.create_superuser("admin", None, password="changeme")
else:
    print(
        "Users detected: this is not a new installation. Skipping super user creation."
    )

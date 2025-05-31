from django.db import models


class CountryChoices(models.TextChoices):
    INDIA = 'IN', 'India'
    UNITED_STATES = 'US', 'United States'
    UNITED_KINGDOM = 'GB', 'United Kingdom'
    AUSTRALIA = 'AU', 'Australia'
    CANADA = 'CA', 'Canada'


class UserTypeChoices(models.TextChoices):
    USER = 'USER', 'USER'
    RESTAURANT_OWNER = 'RESTAURANT_OWNER', 'Restaurant Owner'
    DELIVERY_PARTNER = 'DELIVERY_PARTNER', 'Delivery Partner'

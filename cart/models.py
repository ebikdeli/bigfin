from django.db import models
"""

def discount_hpercent(value: float) -> float:
    if value >= 1.0:
        return value / 100
    return value


class Cart(models.Model):
    profile = models.OneToOneField(to=Profile,
                                   related_name='profile_cart',
                                   on_delete=models.CASCADE)
    # product = models.ManyToManyField(to=Product,
    #                                 related_name='product_cart',
    #                                 blank=True)
    items = models.JSONField(blank=True, default=dict)  # per documents
    total_price = models.PositiveIntegerField(default=0)
    price_after_discount = models.PositiveIntegerField(default=0)
    total_number = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.profile.user.username + '_cart'

class DiscountCode(models.Model):
    code = models.CharField(max_length=5)
    # product = models.ForeignKey(Product,
    #                            related_name='product_discount',
    #                            on_delete=models.CASCADE,
    #                            null=True, blank=True)
    profile = models.ForeignKey(Profile,
                                related_name='profile_discount_code',
                                on_delete=models.CASCADE,
                                null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)
    value = models.PositiveIntegerField(default=0)
    percent = models.FloatField(default=0, validators=[MaxValueValidator(100),
                                                       MinValueValidator(0),
                                                       discount_model_validator])

    def __str__(self):
        return f'discount_code: {self.code}'
"""
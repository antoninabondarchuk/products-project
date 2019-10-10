from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.TextField(max_length=50)
    date = models.DateTimeField()
    link = models.CharField(max_length=200)
    description = models.TextField(max_length=256)
    votes = models.IntegerField(default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def summary(self):
        return self.description[:100]

    def nice_date(self):
        return self.date.strftime('%b %e %Y')

    def __str__(self):
        return f'Product {self.name}: {self.summary}'

    class Meta:
        ordering = ['-votes', '-date']


class Vote(models.Model):
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Vote for {self.product.name} from {self.hunter.username}'



from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User


# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        

class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE,related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=500,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=500,null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
            return url
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=False)
    complete = models.BooleanField(default=False,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200,null=True)
    total = models.FloatField(null=True)
    
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() #lay het tu orderitems
        total = sum([item.quantity for item in orderitems])
        return total
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() #lay het tu orderitems
        total = sum([item.get_total for item in orderitems])
        self.total = total
        self.save()
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=False)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=False)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add = True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


    
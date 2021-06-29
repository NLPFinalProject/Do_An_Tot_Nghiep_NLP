"""from rest_framework import serializers 
from customers.models import Customer
 
 
class CustomerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Customer
        fields = ('username','password')
        """
from rest_framework import serializers

# from User.models import Customer
from UserComponent.models import User

"""class CustomerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Customer
        fields = ('id',
                  'name',
                  'age',
                  'active')"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "name",
            "EmailOrganization",
            "DateOfBirth",
            "is_active",
            "phone",
            "is_lock",
        ]

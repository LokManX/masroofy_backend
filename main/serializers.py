from rest_framework import serializers
from main.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)  
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password) #this will hash the user's password 
        instance.save()
        return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super.to_representation(instance)    
        representation['category'] = CategorySerializer(instance.category)    

class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Transaction
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super.to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['user'] = UserSerializer(instance.user)
        return representation


class IncomeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    class Meta:
        model = Income
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super.to_representation(instance)
        representation['user'] = UserSerializer(instance.user)
        return representation

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset = Product.objects.all())

    class Meta:
        model = Expense
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super.to_representation(instance)
        representation['user'] = UserSerializer(instance.user)
        representation['product'] = ProductSerializer(instance.product)
        return representation

from rest_framework import serializers
from app.models import Definitions, Financials, User


class DictionarySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    title = serializers.CharField()
    definition = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Definitions
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class FinancialsSerializer(serializers.Serializer):
    # user = UserSerializer()
    available_funds = serializers.FloatField()
    funds_held_for_orders = serializers.FloatField()
    portfolio_value = serializers.FloatField()
    timestamp = serializers.DateTimeField()

    class Meta:
        model = Financials
        fields = ['available_funds', 'funds_held_for_orders', 'portfolio_value', 'timestamp']
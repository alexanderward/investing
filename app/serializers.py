from copy import deepcopy

from rest_framework import serializers
from app.models import Definition, Financial, User, SymbolHistory, Symbol


class UserProfileSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplemented()

    def update(self, instance, validated_data):
        if 'notifications' in validated_data.keys():
            notifications = validated_data.pop('notifications', None)
            validated_data['notification_email'] = notifications['email']
            validated_data['notification_sms'] = notifications['sms']

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save(update_fields=validated_data.keys())
        return instance

    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    rh_token = serializers.CharField(required=False)
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_notifications(self, obj):
        return {
            'email': obj.notification_email,
            'sms': obj.notification_sms
        }


class DictionarySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    title = serializers.CharField()
    definition = serializers.CharField()
    category = serializers.CharField()

    class Meta:
        model = Definition
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class FinancialsSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    # user = UserSerializer()
    available_funds = serializers.FloatField()
    funds_held_for_orders = serializers.FloatField()
    portfolio_value = serializers.FloatField()
    timestamp = serializers.DateTimeField()

    class Meta:
        model = Financial
        fields = ['available_funds', 'funds_held_for_orders', 'portfolio_value', 'timestamp']


class SymbolSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.IntegerField()
    symbol = serializers.CharField()
    company = serializers.CharField()
    description = serializers.CharField()
    sector = serializers.CharField()
    industry = serializers.CharField()
    ipo_year = serializers.IntegerField()
    market_cap = serializers.FloatField()
    listed = serializers.BooleanField()
    growth_rate = serializers.FloatField()

    class Meta:
        model = Symbol


class SymbolHistorySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    symbol = SymbolSerializer()
    date = serializers.DateField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    close = serializers.FloatField()
    volume = serializers.IntegerField()

    class Meta:
        model = SymbolHistory

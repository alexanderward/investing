from rest_framework import serializers
from app.models import Definition, Financial, User, SymbolHistory, Symbol


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

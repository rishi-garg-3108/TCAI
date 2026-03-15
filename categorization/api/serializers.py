"""serializer.py
    - It will validate the incoming request JSON
    - Ensures that the required fields are present and correctly formatted
 """
 
from rest_framework import serializers


class HistoricalTransactionSerializer(serializers.Serializer):
    """
    Serializer for historical categorized transactions.
    """

     # Short text describing the past transaction
    description = serializers.CharField(
        required=True,
        max_length=500
    )

    # The category previously assigned to this transaction
    category = serializers.CharField(
        required=True,
        max_length=200
    )


class CompanyContextSerializer(serializers.Serializer):
    """
    Contains company specific context used during categorization.
    """

    # Unique identifier of the company
    company_id = serializers.CharField(
        required=True,
        max_length=100
    )

    # Industry helps the model interpret transactions correctly
    # (e.g., SaaS companies often have many software subscriptions)
    industry = serializers.CharField(
        required=True,
        max_length=200
    )

    # List of valid accounting categories defined by the company
    chart_of_accounts = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=1
    )

    # Historical examples of categorized transactions (it is for few-shot examples)
    historical_transactions = HistoricalTransactionSerializer(
        many=True,
        required=True
    )


class TransactionSerializer(serializers.Serializer):
    """
    Main serializer for the transaction categorization request.
    """

    description = serializers.CharField(
        required=True,
        max_length=500
    )

    vendor = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200
    )

    company_context = CompanyContextSerializer(
        required=True
    )
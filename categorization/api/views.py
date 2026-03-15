"""endpoint that calls the service"""

import json
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TransactionSerializer
from categorization.services.categorization_service import CategorizationService

logger = logging.getLogger("transaction_categorizer")


class CategorizeTransactionView(APIView):
    """
    API endpoint for transaction categorization.
    """

    def post(self, request):

        serializer = TransactionSerializer(data=request.data)

        if not serializer.is_valid():
            logger.warning("Invalid request payload")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            service = CategorizationService()

            # Force plain dict to avoid OrderedDict issues with nested serializer data
            transaction_data = json.loads(json.dumps(serializer.validated_data))

            result = service.categorize_transaction(transaction_data)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Categorization failed: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
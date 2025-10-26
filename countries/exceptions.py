
import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
   
    drf_response = drf_exception_handler(exc, context)

   
    if drf_response is not None:
        status_code = drf_response.status_code

        
        if status_code == status.HTTP_404_NOT_FOUND:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

      
        if status_code == status.HTTP_400_BAD_REQUEST:
            
            details = drf_response.data
            return Response({"error": "Validation failed", "details": details}, status=status.HTTP_400_BAD_REQUEST)

       
        detail = drf_response.data.get("detail") if isinstance(drf_response.data, dict) else drf_response.data
        
        if isinstance(detail, (dict, list)):
            return Response({"error": detail}, status=status_code)
        return Response({"error": str(detail)}, status=status_code)

   
    logger.exception("Unhandled exception in view %s: %s", context.get('view'), exc)
    return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

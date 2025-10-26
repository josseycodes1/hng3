# countryapi/exceptions.py
import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Global DRF exception handler that returns consistent JSON shapes:
    - 404 -> { "error": "Country not found" }
    - 400 -> { "error": "Validation failed", "details": { ... } }
    - 500 -> { "error": "Internal server error" }
    Other APIExceptions will be returned with a compact {"error": "..."}.
    """
    # Let DRF create the standard response first (None if it's an unhandled exception)
    drf_response = drf_exception_handler(exc, context)

    # If DRF produced a response we can map it to the required shape.
    if drf_response is not None:
        status_code = drf_response.status_code

        # 404 -> consistent message per assignment
        if status_code == status.HTTP_404_NOT_FOUND:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        # 400 -> validation-like errors
        if status_code == status.HTTP_400_BAD_REQUEST:
            # Preserve DRF's error details (field-level messages) under "details"
            details = drf_response.data
            return Response({"error": "Validation failed", "details": details}, status=status.HTTP_400_BAD_REQUEST)

        # For other DRF-handled API exceptions (401/403/429/ etc) return compact shape:
        detail = drf_response.data.get("detail") if isinstance(drf_response.data, dict) else drf_response.data
        # If detail is complex (dict/list), keep it as-is under "error"
        if isinstance(detail, (dict, list)):
            return Response({"error": detail}, status=status_code)
        return Response({"error": str(detail)}, status=status_code)

    # If drf_response is None => unhandled exception (500)
    logger.exception("Unhandled exception in view %s: %s", context.get('view'), exc)
    return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

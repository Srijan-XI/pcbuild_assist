"""
Custom exceptions for PCBuild Assist API.
Provides structured error handling with proper HTTP status codes.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException


class APIException(HTTPException):
    """
    Base exception for API errors.
    Provides structured error responses.
    """
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        
        detail = {
            "code": code,
            "message": message,
            "details": self.details
        }
        
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(APIException):
    """Resource not found (404)."""
    def __init__(
        self,
        resource: str,
        identifier: Optional[str] = None,
        message: Optional[str] = None
    ):
        msg = message or f"{resource} not found"
        if identifier:
            msg = f"{resource} with ID '{identifier}' not found"
        
        super().__init__(
            status_code=404,
            code="NOT_FOUND",
            message=msg,
            details={"resource": resource, "identifier": identifier}
        )


class ValidationException(APIException):
    """Validation error (400)."""
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        errors: Optional[list] = None
    ):
        details = {}
        if field:
            details["field"] = field
        if errors:
            details["errors"] = errors
        
        super().__init__(
            status_code=400,
            code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class ServiceUnavailableException(APIException):
    """External service unavailable (503)."""
    def __init__(
        self,
        service: str,
        message: Optional[str] = None,
        retry_after: Optional[int] = None
    ):
        msg = message or f"{service} is temporarily unavailable"
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
        
        super().__init__(
            status_code=503,
            code="SERVICE_UNAVAILABLE",
            message=msg,
            details={"service": service},
            headers=headers if headers else None
        )


class IncompatibleComponentsException(APIException):
    """Components are not compatible (422)."""
    def __init__(
        self,
        component1: str,
        component2: str,
        reason: str
    ):
        super().__init__(
            status_code=422,
            code="INCOMPATIBLE_COMPONENTS",
            message=f"Components are not compatible: {reason}",
            details={
                "component1": component1,
                "component2": component2,
                "reason": reason
            }
        )


class RateLimitException(APIException):
    """Rate limit exceeded (429)."""
    def __init__(
        self,
        limit: str,
        retry_after: int = 60
    ):
        super().__init__(
            status_code=429,
            code="RATE_LIMIT_EXCEEDED",
            message=f"Rate limit exceeded: {limit}",
            details={"limit": limit, "retry_after": retry_after},
            headers={"Retry-After": str(retry_after)}
        )


class AlgoliaException(APIException):
    """Algolia service error (502)."""
    def __init__(
        self,
        operation: str,
        message: Optional[str] = None
    ):
        msg = message or f"Algolia {operation} failed"
        
        super().__init__(
            status_code=502,
            code="ALGOLIA_ERROR",
            message=msg,
            details={"operation": operation}
        )

"""
Structured logging configuration for PCBuild Assist API.
Provides JSON-formatted logs with request tracing.
"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional
import uuid
from contextvars import ContextVar

# Context variable for request tracking
request_id_ctx: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request ID and structured data."""
    
    def format(self, record):
        # Add request ID if available
        record.request_id = request_id_ctx.get() or "no-request"
        
        # Add timestamp in ISO format
        record.timestamp = datetime.utcnow().isoformat() + "Z"
        
        # Format the message
        if hasattr(record, 'extra_data'):
            extra = record.extra_data
        else:
            extra = {}
        
        # Build structured log
        log_data = {
            "timestamp": record.timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": record.request_id,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        if extra:
            log_data["data"] = extra
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # In production, output JSON; in dev, use readable format
        if os.getenv("ENV", "development") == "production":
            import json
            return json.dumps(log_data)
        else:
            # Readable format for development
            extra_str = f" | {extra}" if extra else ""
            return f"[{record.timestamp}] {record.levelname:8} | {record.request_id[:8]:8} | {record.name}: {record.getMessage()}{extra_str}"


class ContextLogger(logging.LoggerAdapter):
    """Logger adapter that adds contextual information."""
    
    def process(self, msg, kwargs):
        # Add extra data if provided
        extra = kwargs.get('extra', {})
        extra['extra_data'] = kwargs.pop('data', {})
        kwargs['extra'] = extra
        return msg, kwargs


def setup_logging(level: str = "INFO") -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Get log level from env or parameter
    log_level = os.getenv("LOG_LEVEL", level).upper()
    
    # Create formatter
    formatter = RequestFormatter()
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def get_logger(name: str) -> ContextLogger:
    """
    Get a logger instance with context support.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        ContextLogger instance
    """
    logger = logging.getLogger(name)
    return ContextLogger(logger, {})


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def set_request_id(request_id: str) -> None:
    """Set the current request ID in context."""
    request_id_ctx.set(request_id)


def get_request_id() -> Optional[str]:
    """Get the current request ID from context."""
    return request_id_ctx.get()

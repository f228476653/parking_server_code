"""Middleware module.

Define MIDDELWARE list.
"""
from app.middlewares.jwt_middleware import jwt_middleware
from app.middlewares.error_middleware import error_middleware

MIDDLEWARES = [
    error_middleware,
    jwt_middleware
    
    
    
]

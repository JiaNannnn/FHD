"""
Core poseidon module for making API calls.

This module provides both synchronous and asynchronous methods
for making API calls to the EnOS API.
"""

import base64
import hashlib
import hmac
import json
import time
import urllib.request
import urllib.parse
import asyncio


def urlopen(access_key, secret_key, url, data=None):
    """
    Make a synchronous API call to the EnOS API.
    
    Args:
        access_key (str): Access key for API authentication
        secret_key (str): Secret key for API authentication
        url (str): URL to call
        data (dict, optional): Data to send in the request. Defaults to None.
        
    Returns:
        dict: Response from the API
    """
    # Create signature
    timestamp = str(int(time.time() * 1000))
    signature = _create_signature(secret_key, timestamp)
    
    # Set up headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'AccessKey {access_key}',
        'timestamp': timestamp,
        'signature': signature
    }
    
    # Convert data to JSON
    data_str = json.dumps(data) if data else None
    data_bytes = data_str.encode('utf-8') if data_str else None
    
    # Create request
    req = urllib.request.Request(url, data=data_bytes, headers=headers)
    
    # Make request
    with urllib.request.urlopen(req) as response:
        response_data = response.read().decode('utf-8')
        return json.loads(response_data)


def _raw_request(access_key, secret_key, url, data=None):
    """
    Make a raw HTTP request to the API without JSON parsing.
    
    This is useful for testing connectivity and debugging.
    
    Args:
        access_key (str): Access key for API authentication
        secret_key (str): Secret key for API authentication
        url (str): URL to call
        data (dict, optional): Data to send in the request. Defaults to None.
        
    Returns:
        http.client.HTTPResponse: Raw HTTP response object
    """
    # Create signature
    timestamp = str(int(time.time() * 1000))
    signature = _create_signature(secret_key, timestamp)
    
    # Set up headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'AccessKey {access_key}',
        'timestamp': timestamp,
        'signature': signature
    }
    
    # Convert data to JSON
    data_str = json.dumps(data) if data else None
    data_bytes = data_str.encode('utf-8') if data_str else None
    
    # Create request
    req = urllib.request.Request(url, data=data_bytes, headers=headers)
    
    # Make request but don't parse response
    return urllib.request.urlopen(req)


async def a_urlopen(access_key, secret_key, url, data=None):
    """
    Make an asynchronous API call to the EnOS API.
    
    This is a custom addition to the poseidon library that provides
    asynchronous API call functionality.
    
    Args:
        access_key (str): Access key for API authentication
        secret_key (str): Secret key for API authentication
        url (str): URL to call
        data (dict, optional): Data to send in the request. Defaults to None.
        
    Returns:
        dict: Response from the API
    """
    # In a real async implementation, we would use aiohttp or httpx
    # For simplicity, we're running the synchronous version in an executor
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, 
        lambda: urlopen(access_key, secret_key, url, data)
    )
    return result


def _create_signature(secret_key, timestamp):
    """
    Create a signature for API authentication.
    
    Args:
        secret_key (str): Secret key for API authentication
        timestamp (str): Current timestamp
        
    Returns:
        str: Signature for API authentication
    """
    # Convert secret key to bytes
    key = secret_key.encode('utf-8')
    
    # Create message (timestamp)
    message = timestamp.encode('utf-8')
    
    # Create signature
    signature = hmac.new(key, message, hashlib.sha256).digest()
    
    # Encode as base64
    return base64.b64encode(signature).decode('utf-8') 
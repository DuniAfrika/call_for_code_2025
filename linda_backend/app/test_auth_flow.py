#!/usr/bin/env python3
"""Test script for WhatsApp authentication flow."""

from services.whatsapp_auth import (
    process_whatsapp_message_for_auth,
    get_message_count,
    increment_message_count
)

def test_auth_flow():
    """Test the authentication flow with a sample phone number."""
    test_phone = "+1234567890"
    
    print("🧪 Testing WhatsApp Authentication Flow")
    print("=" * 50)
    
    # Test message 1
    print(f"\n📱 Message 1 from {test_phone}")
    result1 = process_whatsapp_message_for_auth(test_phone, "Hello")
    print(f"Message count: {result1['message_count']}")
    print(f"Authenticated: {result1['authenticated']}")
    if result1.get('response'):
        print(f"Response: {result1['response']['text']['body']}")
    
    # Test message 2
    print(f"\n📱 Message 2 from {test_phone}")
    result2 = process_whatsapp_message_for_auth(test_phone, "How are you?")
    print(f"Message count: {result2['message_count']}")
    print(f"Authenticated: {result2['authenticated']}")
    if result2.get('response'):
        print(f"Response: {result2['response']['text']['body']}")
    
    # Test message 3 (should trigger registration prompt)
    print(f"\n📱 Message 3 from {test_phone}")
    result3 = process_whatsapp_message_for_auth(test_phone, "Safety question")
    print(f"Message count: {result3['message_count']}")
    print(f"Authenticated: {result3['authenticated']}")
    if result3.get('response'):
        print(f"Response: {result3['response']['text']['body']}")
    
    # Test registration response
    print(f"\n📱 Registration response from {test_phone}")
    result4 = process_whatsapp_message_for_auth(test_phone, "John Doe")
    print(f"Message count: {result4['message_count']}")
    print(f"Authenticated: {result4['authenticated']}")
    if result4.get('response'):
        print(f"Response: {result4['response']['text']['body']}")
    
    # Test authenticated message
    print(f"\n📱 Authenticated message from {test_phone}")
    result5 = process_whatsapp_message_for_auth(test_phone, "Safety question")
    print(f"Message count: {result5['message_count']}")
    print(f"Authenticated: {result5['authenticated']}")
    if result5.get('response'):
        print(f"Response: {result5['response']['text']['body']}")

if __name__ == "__main__":
    test_auth_flow() 
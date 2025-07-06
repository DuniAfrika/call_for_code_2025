#!/usr/bin/env python3
"""Simple test script for WhatsApp authentication flow without external dependencies."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock the external dependencies
class MockUser:
    def __init__(self, phone, full_name=None):
        self.phone = phone
        self.full_name = full_name
        self.username = f"whatsapp_{phone.replace('+', '').replace('-', '')}"
        self.email = f"{self.username}@whatsapp.local"
        self.isAdmin = False
        self.isActive = True
        self.hashed_password = None

# Mock the database functions
def mock_get_user_by_phone(phone):
    return None  # Simulate no existing user

def mock_create_whatsapp_user(phone, full_name):
    return MockUser(phone, full_name)

# Import and patch the auth module
import services.whatsapp_auth as auth_module

# Patch the functions
auth_module.get_user_by_phone = mock_get_user_by_phone
auth_module.create_whatsapp_user = mock_create_whatsapp_user

def test_auth_flow():
    """Test the authentication flow with a sample phone number."""
    test_phone = "+1234567890"
    
    print("🧪 Testing WhatsApp Authentication Flow (Simplified)")
    print("=" * 60)
    
    # Test message 1
    print(f"\n📱 Message 1 from {test_phone}")
    result1 = auth_module.process_whatsapp_message_for_auth(test_phone, "Hello")
    print(f"Message count: {result1['message_count']}")
    print(f"Authenticated: {result1['authenticated']}")
    if result1.get('response'):
        print(f"Response: {result1['response']['text']['body']}")
    
    # Test message 2
    print(f"\n📱 Message 2 from {test_phone}")
    result2 = auth_module.process_whatsapp_message_for_auth(test_phone, "How are you?")
    print(f"Message count: {result2['message_count']}")
    print(f"Authenticated: {result2['authenticated']}")
    if result2.get('response'):
        print(f"Response: {result2['response']['text']['body']}")
    
    # Test message 3 (should trigger registration prompt)
    print(f"\n📱 Message 3 from {test_phone}")
    result3 = auth_module.process_whatsapp_message_for_auth(test_phone, "Safety question")
    print(f"Message count: {result3['message_count']}")
    print(f"Authenticated: {result3['authenticated']}")
    if result3.get('response'):
        print(f"Response: {result3['response']['text']['body']}")
    
    # Test registration response
    print(f"\n📱 Registration response from {test_phone}")
    result4 = auth_module.process_whatsapp_message_for_auth(test_phone, "John Doe")
    print(f"Message count: {result4['message_count']}")
    print(f"Authenticated: {result4['authenticated']}")
    if result4.get('response'):
        print(f"Response: {result4['response']['text']['body']}")
    
    # Test authenticated message
    print(f"\n📱 Authenticated message from {test_phone}")
    result5 = auth_module.process_whatsapp_message_for_auth(test_phone, "Safety question")
    print(f"Message count: {result5['message_count']}")
    print(f"Authenticated: {result5['authenticated']}")
    if result5.get('response'):
        print(f"Response: {result5['response']['text']['body']}")
    
    print("\n✅ Authentication flow test completed!")

if __name__ == "__main__":
    test_auth_flow() 
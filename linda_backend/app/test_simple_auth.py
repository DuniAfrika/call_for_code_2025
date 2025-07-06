#!/usr/bin/env python3
"""Simple test for immediate WhatsApp authentication flow."""

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

def test_simple_auth_flow():
    """Test the simplified authentication flow."""
    test_phone = "+1234567890"
    
    print("🧪 Testing Simplified WhatsApp Authentication Flow")
    print("=" * 60)
    
    # Test first message (should prompt for registration)
    print(f"\n📱 First message from {test_phone}")
    result1 = auth_module.process_whatsapp_message_for_auth(test_phone, "Hello")
    print(f"Authenticated: {result1['authenticated']}")
    if result1.get('response'):
        print(f"Response: {result1['response']['text']['body']}")
    
    # Test registration response
    print(f"\n📱 Registration response from {test_phone}")
    result2 = auth_module.process_whatsapp_message_for_auth(test_phone, "John Doe")
    print(f"Authenticated: {result2['authenticated']}")
    if result2.get('response'):
        print(f"Response: {result2['response']['text']['body']}")
    
    # Test authenticated message
    print(f"\n📱 Authenticated message from {test_phone}")
    result3 = auth_module.process_whatsapp_message_for_auth(test_phone, "Safety question")
    print(f"Authenticated: {result3['authenticated']}")
    if result3.get('response'):
        print(f"Response: {result3['response']['text']['body']}")
    
    print("\n✅ Simplified authentication flow test completed!")

if __name__ == "__main__":
    test_simple_auth_flow() 
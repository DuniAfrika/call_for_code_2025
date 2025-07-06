"""WhatsApp Authentication Service for lazy user registration."""

import json
import os
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from app.db.config import get_session
from app.users.models import User
from app.users.utils import create_access_token
from datetime import datetime, timedelta

# In-memory storage for message counts (in production, use Redis or database)
message_counts: Dict[str, int] = {}
pending_registrations: Dict[str, Dict[str, Any]] = {}

def get_message_count(phone: str) -> int:
    """Get the message count for a phone number."""
    return message_counts.get(phone, 0)

def increment_message_count(phone: str) -> int:
    """Increment message count for a phone number."""
    current_count = message_counts.get(phone, 0)
    message_counts[phone] = current_count + 1
    return current_count + 1

def get_user_by_phone(phone: str) -> Optional[User]:
    """Get user by phone number from database."""
    db = next(get_session())
    try:
        return db.exec(select(User).where(User.phone == phone)).first()
    finally:
        db.close()

def create_whatsapp_user(phone: str, full_name: str) -> User:
    """Create a new user from WhatsApp registration."""
    db = next(get_session())
    try:
        # Generate a simple username from phone number
        username = f"whatsapp_{phone.replace('+', '').replace('-', '')}"
        
        # Create user without password (WhatsApp users don't need passwords)
        user = User(
            username=username,
            full_name=full_name,
            phone=phone,
            email=f"{username}@whatsapp.local",  # Placeholder email
            isAdmin=False,
            isActive=True,
            hashed_password=""  # No password for WhatsApp users
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def should_prompt_for_registration(phone: str) -> bool:
    """Check if user should be prompted for registration (after 3 messages)."""
    count = get_message_count(phone)
    return count >= 3 and get_user_by_phone(phone) is None

def is_registration_pending(phone: str) -> bool:
    """Check if user is in the process of registration."""
    return phone in pending_registrations

def set_registration_pending(phone: str, data: Dict[str, Any]) -> None:
    """Mark user as pending registration."""
    pending_registrations[phone] = data

def get_registration_data(phone: str) -> Optional[Dict[str, Any]]:
    """Get pending registration data for a phone number."""
    return pending_registrations.get(phone)

def complete_registration(phone: str) -> None:
    """Remove user from pending registrations."""
    if phone in pending_registrations:
        del pending_registrations[phone]

def create_whatsapp_token(phone: str) -> str:
    """Create a JWT token for WhatsApp user."""
    return create_access_token(data={"sub": phone})

def process_whatsapp_message_for_auth(phone: str, message_text: str) -> Dict[str, Any]:
    """
    Process WhatsApp message for authentication flow.
    Returns response data and authentication status.
    """
    # Increment message count
    message_count = increment_message_count(phone)
    
    # Check if user exists
    user = get_user_by_phone(phone)
    
    if user:
        # User is already registered
        return {
            "authenticated": True,
            "user": user,
            "response": None,  # No special response needed
            "message_count": message_count
        }
    
    # Check if we should prompt for registration
    if should_prompt_for_registration(phone):
        if not is_registration_pending(phone):
            # First time prompting for registration
            set_registration_pending(phone, {"step": "name_request"})
            return {
                "authenticated": False,
                "user": None,
                "response": {
                    "to": phone,
                    "text": {
                        "body": "Welcome! I'm your safety assistant. To provide you with personalized safety recommendations, I need to know your name. Please reply with your full name."
                    }
                },
                "message_count": message_count
            }
        else:
            # User is in registration process
            registration_data = get_registration_data(phone)
            
            if registration_data.get("step") == "name_request":
                # User provided their name
                full_name = message_text.strip()
                if len(full_name) < 2:
                    return {
                        "authenticated": False,
                        "user": None,
                        "response": {
                            "to": phone,
                            "text": {
                                "body": "Please provide your full name (at least 2 characters)."
                            }
                        },
                        "message_count": message_count
                    }
                
                # Create the user
                try:
                    user = create_whatsapp_user(phone, full_name)
                    complete_registration(phone)
                    
                    return {
                        "authenticated": True,
                        "user": user,
                        "response": {
                            "to": phone,
                            "text": {
                                "body": f"Thank you, {full_name}! You're now registered. I'm here to help you with workplace safety. What safety concerns do you have today?"
                            }
                        },
                        "message_count": message_count
                    }
                except Exception as e:
                    return {
                        "authenticated": False,
                        "user": None,
                        "response": {
                            "to": phone,
                            "text": {
                                "body": "Sorry, there was an error creating your account. Please try again later."
                            }
                        },
                        "message_count": message_count
                    }
    
    # User hasn't reached registration threshold yet
    return {
        "authenticated": False,
        "user": None,
        "response": None,  # No special response needed
        "message_count": message_count
    } 
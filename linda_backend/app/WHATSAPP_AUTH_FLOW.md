# WhatsApp Authentication Flow

## Overview

The Linda Backend now implements a **lazy authentication system** for WhatsApp users. Users are identified by their WhatsApp phone number and are prompted to register after sending 3 messages.

## Flow Description

### 1. Initial Messages (Messages 1-2)
- User sends messages via WhatsApp
- System tracks message count per phone number
- User receives simple responses without AI processing
- No registration required yet

### 2. Registration Prompt (Message 3)
- After 3 messages, unregistered users are prompted for their name
- System sends: *"Welcome! I'm your safety assistant. To provide you with personalized safety recommendations, I need to know your name. Please reply with your full name."*

### 3. Registration Process
- User provides their full name
- System validates name (minimum 2 characters)
- Creates user account with:
  - Username: `whatsapp_{phone_number}`
  - Email: `{username}@whatsapp.local`
  - No password (WhatsApp users don't need passwords)
  - Phone number from WhatsApp

### 4. Post-Registration
- User receives confirmation message
- All subsequent messages are processed with AI
- User is fully authenticated

## Technical Implementation

### Key Files

1. **`services/whatsapp_auth.py`**
   - Core authentication logic
   - Message counting
   - Registration flow management
   - User creation for WhatsApp users

2. **`api/whatsapp_utils.py`**
   - Updated to integrate authentication
   - Handles both text and image messages
   - Routes messages based on authentication status

3. **`users/models.py`**
   - Updated User model to support optional passwords
   - WhatsApp users have `hashed_password = None`

### Authentication States

1. **Unregistered (< 3 messages)**
   - Simple responses
   - No AI processing
   - Message count tracking

2. **Registration Pending (3+ messages, no name)**
   - Prompt for name
   - Validation of name input
   - User creation process

3. **Authenticated (Registered)**
   - Full AI processing
   - Safety recommendations
   - Image analysis

## API Endpoints

### Check User Status
```
GET /users/whatsapp/{phone}
```

### Detailed Auth Status
```
GET /users/whatsapp/{phone}/auth-status
```

## Data Storage

### In-Memory Storage (Development)
- `message_counts`: Tracks message count per phone
- `pending_registrations`: Tracks registration state

### Database Storage
- User accounts created in database
- No passwords for WhatsApp users
- Phone number as primary identifier

## Security Considerations

1. **Phone Number Validation**: WhatsApp provides verified phone numbers
2. **No Password Storage**: WhatsApp users don't need passwords
3. **JWT Tokens**: Used for API authentication when needed
4. **Message Tracking**: Simple in-memory tracking (use Redis in production)

## Production Considerations

1. **Redis**: Replace in-memory storage with Redis for message counts
2. **Database**: Add message logging table
3. **Rate Limiting**: Implement rate limiting per phone number
4. **Error Handling**: Add more robust error handling
5. **Logging**: Add comprehensive logging for debugging

## Testing

Run the test script to verify the flow:
```bash
python test_auth_flow.py
```

This will simulate the complete authentication flow with a test phone number. 
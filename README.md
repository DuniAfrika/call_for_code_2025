# 🌞 Jua Kali Bot

**Jua Kali Bot** is a powerful FastAPI-based application built to integrate with **WhatsApp/META APIs** and **AI models** for dynamic messaging, image processing, and intelligent recommendations.

---

## 📁 Project Structure

```
juakali-bot/
│
├── app/                         # Core application logic
│   ├── api/                     # WhatsApp/META API & Webhooks
│   │   ├── webhook_handler.py
│   │   └── whatsapp_utils.py
│   │
│   ├── services/                # Business logic
│   │   ├── user_service.py
│   │   ├── image_processor.py   # Integrates with AI model
│   │   └── recommendation.py
│   │
│   ├── ai_clients/              # AI integrations
│   │   ├── granite_vision.py    # Vision model integration
│   │   └── granite_llm.py       # Optional LLM for text processing
│   │
│   ├── db/                      # Database models and queries
│   │   ├── models.py
│   │   └── queries.py
│   │
│   ├── utils/                   # Helper functions and validations
│   │   ├── input_validator.py
│   │   ├── logger.py
│   │   └── session_manager.py
│   │
│   └── main.py                  # Application entrypoint
│
├── config/                      # Configuration files
│   ├── settings.py
│   └── secrets.env
│
├── tests/                       # Unit and integration tests
│   ├── test_image_processor.py
│   └── test_webhook_handler.py
│
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
└── run.sh                       # Start server script
```

---

## 🚀 Features

- ✅ **Webhook Integration**  
  Handles WhatsApp webhook verification and message processing.

- 🧠 **AI Vision Model**  
  Processes user-submitted images using a pre-trained vision model.

- 💬 **Smart Message Handling**  
  Supports both text and image messages with automated, intelligent replies.

- 🎯 **Recommendation Engine**  
  Provides helpful suggestions based on user input and activity.

- 🔐 **Secure Configuration**  
  Uses `.env` files to manage API tokens and environment settings safely.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd juakali-bot
```

### 2. Install Dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

---

## 🧪 Running the Bot

Use the provided script to start the server:

```bash
bash run.sh
```

Or run the FastAPI app manually via:

```bash
uvicorn app.main:app --reload
```

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit a pull request.

---


---

> Built with ❤️  for the informal sector by the DuniAfrika team.

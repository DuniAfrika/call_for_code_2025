Jua Kali
===============================

juakali-bot/
│
├── 📁 app/                      # Core application logic
│   ├── 📁 api/                  # WhatsApp/META API & Webhooks
│   │   └── webhook_handler.py  
│   │   └── whatsapp_utils.py
│   │
│   ├── 📁 services/             # Business logic
│   │   └── user_service.py
│   │   └── image_processor.py  # Integrates with AI model
│   │   └── recommendation.py
│   │
│   ├── 📁 ai_clients/           # AI integrations
│   │   └── granite_vision.py   # Call to Vision model
│   │   └── granite_llm.py      # Optional, if using LLM for text
│   │
│   ├── 📁 db/                   # DB models and queries
│   │   └── models.py
│   │   └── queries.py
│   │
│   ├── 📁 utils/                # Helper functions and validations
│   │   └── input_validator.py
│   │   └── logger.py
│   │   └── session_manager.py
│   │
│   └── main.py                 # Entrypoint (e.g. Flask app or FastAPI)
│
├── 📁 config/                  # Configuration (env vars, tokens)
│   └── settings.py
│   └── secrets.env
│
├── 📁 tests/                   # Unit and integration tests
│   └── test_image_processor.py
│   └── test_webhook_handler.py
│
├── requirements.txt           # Dependencies
├── README.md
└── run.sh                     # Script to start the server


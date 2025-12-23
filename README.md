# 🚀 Certificate-Based Notification Receiver

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

A sleek and secure Flask-based server designed to receive and process certificate-based HTTP notifications. Perfect for handling webhook payloads with built-in logging and health checks.

## ✨ Features

- 🔒 **Secure Notifications**: Handles certificate-based authentication for incoming requests
- 📡 **Webhook Receiver**: Dedicated `/notify` endpoint for notification payloads
- 🏥 **Health Monitoring**: Built-in health check endpoint
- 🐳 **Docker Ready**: Containerized deployment with Docker Compose
- 📝 **Comprehensive Logging**: Logs all incoming notifications for auditing
- ⚡ **Lightweight**: Minimal dependencies, fast startup

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (for containerized deployment)

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/stapankumar/receiver.git
   cd receiver
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.dummy` to `.env`
   - Update the values in `.env` with your actual database credentials

4. Run the server:
   ```bash
   python server.py
   ```

### Docker Deployment
1. Set up your `.env` file as described above
2. Build and run:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

## 📖 Usage

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/notify` | Receives notification data (expects JSON payload) |
| `GET` | `/` | Health check endpoint |

### Example Request
```bash
curl -X POST http://localhost:5000/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Certificate notification", "data": "..."}'
```

### Health Check
```bash
curl http://localhost:5000/
#returns: {"status": "healthy"}
```

## 🚀 Deployment

### Render (Free HTTPS)
Deploy effortlessly on [Render](https://render.com/) for a free HTTPS URL with automatic TLS certificates.

### Docker Compose
For local testing or production deployment:
```yaml
#docker-compose.yaml
version: '3.8'
services:
  receiver:
    build: .
    ports:
      - "5000:5000"
```

## 📊 Database

The application uses a SQLite database initialized with `init.sql` for storing notification logs.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

Made with ❤️ by [stapankumar](https://github.com/stapankumar)

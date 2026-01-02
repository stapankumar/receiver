# Certificate-Based Notification Receiver

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)

A sleek and secure Flask-based server designed to receive and process certificate-based HTTP notifications. Perfect for handling webhook payloads with built-in logging and health checks.

## Features

- **Secure Notifications**: Handles certificate-based authentication for incoming requests
- **Webhook Receiver**: Dedicated `/notify` endpoint for notification payloads
- **Health Monitoring**: Built-in health check endpoint
- **Docker Ready**: Containerized deployment with Docker Compose
- **Comprehensive Logging**: Logs all incoming notifications for auditing
- **Lightweight**: Minimal dependencies, fast startup

## Installation

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (for containerized deployment)

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/stapankumar/receiver.git
   cd receiver
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  #on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.dummy` to `.env` (if not already present)
   - Update the values in `.env` with your actual database credentials

5. Run the server:
   ```bash
   python server.py
   ```

### Docker Deployment

#### Using Docker Compose

1. Set up your `.env` file as described above
2. Build and run:
   ```bash
   docker compose build
   docker compose up -d
   ```

#### Building and Exporting Image for Kubernetes

Set up your `.env` file as described above.

Build the Docker image:

```bash
docker build -t nads:1.0.0 .
```

Where:
- `nads` = Notification Aggregator and Data Service
- `1.0.0` = version

Save the Docker image as a tarball:

```bash
docker save -o nads:1.0.0.tar nads:1.0.0
gzip nads:1.0.0.tar   # optional: compress to nads-1.0.0.tar.gz
```

Load the image on another machine:

```bash
gunzip -c nads:1.0.0.tar.gz | docker load
```

Run the container:

```bash
docker run -it --rm nads:1.0.0
```

Optional one-liner to build → save → compress in a single step:

```bash
docker build -t nads:1.0.0 . && docker save nads:1.0.0 | gzip > nads-1.0.0.tar.gz
```

## Usage

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

## Extending the Application

This application is designed to be easily extensible, allowing you to add new notification types, endpoints, and database schemas with minimal effort. Here's how to add a new feature:

### Adding a Custom Schema

1. **Create a new table**: Use the `create_schema.py` script to add a new table to the database. Modify the SQL query in the `run_sql()` function to define your new table schema. For example, to create a table for village notifications:

2. **Run the script**: Execute the script to apply the changes to the database:
   ```bash
   python create_schema.py
   ```

### Adding a New Endpoint in server.py

1. **Import necessary functions**: Ensure you import any required functions from `db.notifications_repo` and `parser.notification_parser`.

2. **Define the endpoint**: Add a new route in `server.py`. For example, to add a `/notify/village` endpoint:

   ```python
   @app.route("/notify/village", methods=["POST"])
   def receive_village():
       try:
           payload = request.get_data(as_text=True)
           #insert into the new table
           insert_village_notification(
               request.path,
               request.method,
               request.headers,
               payload
           )
           print("Village Notification stored", flush=True)
       except Exception as e:
           print(f"Failed to decode payload: {e}", flush=True)

       return "", 200
   ```

3. **Add fetch methods**: Create GET endpoints to retrieve notifications. For example:

   ```python
   @app.route("/village", methods=["GET"])
   def get_parsed_village_data():
       rows = fetch_recent_village(50)
       
       parsed_results = []
       for r in rows:
           parsed_con = parse_village_notification_payload(r[1])
           response_obj = {}
           if isinstance(parsed_con, dict):
               response_obj.update(parsed_con)
           response_obj["notification_id"] = r[0]
           response_obj["received_at"] = r[2].isoformat()
           parsed_results.append(response_obj)

       return jsonify(parsed_results)
   ```

### Fetching and Inserting Notifications

- **Inserting**: Use functions like `insert_notification` or create custom ones in `db/notifications_repo.py`. Pass the path, method, headers, and payload to store in the database.

- **Fetching**: Create functions to retrieve data, such as `fetch_recent` or custom variants. Use SQL queries to select from your new table and return the results.

- **Parsing**: Add custom parsers in `parser/notification_parser.py` or create new files like `village_parser.py` to handle specific payload structures.

This modular approach makes it simple to extend the application for new use cases without modifying core functionality.

## Deployment

### Render (Free HTTPS)
Deploy effortlessly on [Render](https://render.com/) for a free HTTPS URL with automatic TLS certificates.


## Database

The application uses a PostgreSQL database initialized with `init.sql` for storing notification logs. Use `create_schema.py` to add custom tables for new notification types.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Support

If you have any questions or issues, please open an issue on GitHub.

---

Made with ❤️ by [stapankumar](https://github.com/stapankumar)

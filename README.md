# Marketplace Events Integration and Backend Service

This repository includes two applications designed for managing marketplace events data: a FastAPI application for integrating with marketplace APIs and a Django-based backend service for storing and querying event data.

## 1. FastAPI Application

The FastAPI application handles:

- Periodically polling marketplace events APIs.
- Parsing and formatting the fetched event data.
- Sending API calls to the backend service to store events in the database.

## 2. Django Backend Service

The Django backend service offers:

- APIs to save marketplace events data to the database.
- Client-facing APIs for querying events data.
- Cached API responses for improved performance.
- **[Client-facing API Documentation](http://localhost:8000/swagger/)**

## Key Features

- **Efficient Data Retrieval**: Fetches events dynamically based on specified start and end times using RESTful endpoints.
- **Caching**: Implements caching to speed up repeated data requests.
- **Asynchronous Support**: Uses asynchronous programming for database and network operations to enhance I/O efficiency.
- **Scalability**: Capable of handling 1,000 to 5,000 requests per minute, suitable for high-load scenarios.

## 🎯 Project Structure and Division

The project is divided into two parts for clarity and scalability:

- **Dedicated Polling Service:** The FastAPI application operates as a standalone polling service for marketplace events, ensuring independent scalability and flexibility in handling various marketplace APIs.
- **Robust Client-Facing Backend:** The Django backend focuses on providing a scalable and robust API for storing and querying event data, leveraging Django's ORM for reliable data management.

## Technologies Used

- **Django**: A high-level Python web framework that promotes rapid development and clean design. It includes features like an ORM, admin interface, authentication, and routing.
- **Django REST Framework (DRF)**: A powerful toolkit for building web APIs with Django, offering serializers, authentication, pagination, and more.
- **FastAPI**: A modern, high-performance web framework for building APIs.
- **HTTPX**: A fully-featured HTTP client for Python 3, providing both synchronous and asynchronous APIs.

## Project Structure

```plaintext
├── EventsMarketPlace/ # Django-based client-facing API app
│ ├── events/ # Events functionality
└── polling_app/ # FastAPI-based polling app
└── README.md
└── requirements.txt
```

## Setup and Installation

### Prerequisites

- Python 3.8+

### Installation Steps

1. **Clone the repository**

2. **Install dependencies**

   ```bash
   pip install --user -r requirements.txt
   ```

3. **Configure the environment**

   Adjust the `settings.py` file in the Django project as needed.

4. **Run the applications**

   Start the Django server:

   ```bash
   python EventsMarketPlace/manage.py runserver
   ```

   Start the FastAPI server:

   ```bash
   python polling_app/main.py
   ```

## Usage

Access the API through the following endpoints:

- **API Documentation**: Visit `http://localhost:8000/swagger` to access the Swagger UI for interactive API documentation.
- **Django Admin Panel**: Visit `http://localhost:8000/admin` and use the credentials `username=fmadmin` and `password=fevermarket`.

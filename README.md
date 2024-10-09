# User and Group Management API

This FastAPI application provides an API for managing users, groups, and group memberships using an in-memory SQLite database. The API allows creating, updating, and deleting users and groups, as well as managing user memberships within groups.

## Setup and Run the Application

### Prerequisites

- Python 3.8+
- `pip` (Python package manager)

### Setup

1. **Clone the Repository**:

```
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **Create a virtual environment**

```
python -m venv venv
source venv/bin/activate
```

3. **Install required modules**

```
pip install -r requirements.txt
```

4. **Run the application**

```
uvicorn main:app --reload
```

The application will by default run on http://127.0.0.1:8000.

## Using the API

The API can be used with e.g. curl. For example, adding a user:

```
curl -X POST http://127.0.0.1:8000/v1/users/ -H "Content-Type: application/json" -d '{"username": "testuser", "email": "testuser@example.com"}'
```

Once the application is running, you can explore the API and test its endpoints via the OpenAPI interactive documentation (Swagger UI) at: http://127.0.0.1:8000/docs.

## Development
### Testing with pytest

This application uses pytest for testing. The test suite includes unit tests for ensuring the correct behavior of the API endpoints. Run the test suite with:

```
pytest
```

### Linting

Linting and type checking can be done with

```
pflake8
mypy
```



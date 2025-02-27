# FastAPI Blogs Backend

This is a FastAPI backend for a blogging platform. It provides APIs for managing users, posts, comments, and authentication.

## Features
- FastAPI framework for high-performance APIs
- PostgreSQL database
- Authentication and authorization
- CRUD operations for blogs and users
- Docker support

## Prerequisites
Ensure you have the following installed:
- Python 3.11+
- Docker & Docker Compose

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/xinyingfan13/blog-backend-fastapi.git
   cd blog-backend-fastapi
   ```
2. Create and update the `.env` file with database credentials:
   ```sh
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name
   ```
3. Set environments to local
    ```
   export $(cat .env | xargs)
   ```
4. Start the database using Docker Compose:
   ```sh
   docker-compose up -d
   ```
5. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
6. Run database migrations:
   ```sh
   alembic upgrade head
   ```
7. Start the FastAPI server:
   ```sh
   uvicorn app.main:app --reload
   ```

## API Documentation
Once the server is running, access the interactive API docs at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Running Tests
Run the test suite using:
```sh
pytest
```

## License
This project is licensed under the MIT License.

---

Happy coding! 🚀


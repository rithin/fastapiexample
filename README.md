# fastapiexample

#install below 

pip install fastapi[all] uvicorn sqlalchemy databases[postgresql] python-dotenv
pip install psycopg2-binary

Here's what each package is used for:

fastapi[all]: FastAPI framework with all optional dependencies.
uvicorn: ASGI server to run the FastAPI application.
sqlalchemy: SQL toolkit and Object-Relational Mapping (ORM) library.
databases[postgresql]: Database support for FastAPI using SQLAlchemy and databases with PostgreSQL.
python-dotenv: Package for managing environment variables using a .env file.
Make sure to run this command in your project's virtual environment. Additionally, you might need to install psycopg2 for PostgreSQL database support. You can install it separately:


#postgres

CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

#mysql

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT
);

#Run and test the app

uvicorn main:app --reload

#Visit

http://127.0.0.1:8000
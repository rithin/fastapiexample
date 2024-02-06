# fastapiexample

#install below 

pip3 install fastapi[all] sqlalchemy psycopg2

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
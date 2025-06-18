from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import datetime
import mysql.connector as db
from sha1encrypt import encrypt_password
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


def get_db_connection():
    connection = db.connect(
        host= "sql200.infinityfree.com",   #'localhost',
        user="if0_39263752",  #'root',
        password="pEYMqZn4F3",   #'',
        database= "if0_39263752_check_io"   #'check_io'
    )
    return connection


class SignUpSchema(BaseModel):
    name: str
    password: str
    email: str


@app.post("/signup")
def sign_up(request: SignUpSchema):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
    user = cursor.fetchone()
    if user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail='Email already exists')

    payload = {
        'email': request.email,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration tim
    }

    # Encode the JWT token
    token = jwt.encode(payload, '123', algorithm='HS256')

    cursor.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)",
                   (request.name, encrypt_password(request.password), request.email))
    connection.commit()
    cursor.close()
    connection.close()
    return {"token": token}


class SignINSchema(BaseModel):
    email: str
    password: str
     


@app.post("/signin")
def sign_in(request: SignINSchema):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=404, detail='Email not found')

    stored_password = user[2]  # Assuming the third column is the password
    if encrypt_password(request.password)!=stored_password:
        cursor.close()
        connection.close()
        raise HTTPException(status_code=401, detail='Incorrect password')

    payload = {
        'email': request.email,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
    }

    # Encode the JWT token
    token = jwt.encode(payload, '123', algorithm='HS256')

    cursor.close()
    connection.close()
    return {"token": token}
    


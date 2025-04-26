from fastapi import APIRouter, Depends, HTTPException
import logging
from src.db import get_db_connection
from src.schemas import UserResponse, LoginRequest

router = APIRouter()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/auth/login", response_model=UserResponse)
def login(login_data: LoginRequest):
    logger.info(f"Login attempt - username: {login_data.username}")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM frog_cafe.users WHERE name = %s AND pass = %s"
    cur.execute(query, (login_data.username, login_data.password))
    user = cur.fetchone()
    
    cur.close()
    conn.close()

    if not user:
        logger.warning(f"Invalid credentials for user: {login_data.username}")
        raise HTTPException(status_code=401, detail="Вы кто такой? Я вас не звал")

    return {
        "id": user["id"],
        "name": user["name"],
        "role_id": user["role_id"]
    }
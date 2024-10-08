from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Callable
import sqlite3
import logging
import logging.config

conn = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.warning('Starting up')
    conn = get_db()
    yield
    conn.close()


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

logconfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console', 'file_handler'],
        'level': 'DEBUG',
    },
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s %(levelname)s %(message)s',
            'datefmt': '%d.%m.%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'INFO'
        },
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': 'app.log',
            'level': 'DEBUG'
        }
    },
}

logging.config.dictConfig(logconfig)
logger = logging.getLogger('main')


# Database connection function
def get_db() -> sqlite3.Connection:
    # For in-memory database:
    global conn
    if conn is None:
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        # conn = sqlite3.connect("data/groups.db")
        init_db(conn)
        conn.row_factory = sqlite3.Row  # Return rows as dictionary-like objects
    return conn


def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    logger.warning('Starting up')

    with open('sql/groups_users.ddl', 'r', encoding='utf8') as sqlfile:
        sqldata = sqlfile.read()
        cursor.executescript(sqldata)

    conn.commit()


# Dependency to use the database connection
def get_db_dependency(db: Callable[[], sqlite3.Connection] = get_db):
    return db()


# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    email: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class GroupCreate(BaseModel):
    group_name: str


class GroupUpdate(BaseModel):
    group_name: Optional[str] = None


class MembershipCreate(BaseModel):
    user_id: int
    role: Optional[str] = "member"


# USERS


@app.post("/v1/users/", response_model=dict)
def add_user(user: UserCreate):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (user.username, user.email))
        conn.commit()
        return {"message": "User added successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")
#    finally:
#        conn.close()


@app.put("/v1/users/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserUpdate):
    cursor = conn.cursor()

    updates = []
    params = []

    # if user.username:
    #     updates.append("username = ?")
    #     params.append(user.username)

    if user.email:
        updates.append("email = ?")
        params.append(user.email)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    params.append(user_id)

    query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"

    cursor.execute(query, params)
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User updated successfully"}


@app.delete("/v1/users/{user_id}", response_model=dict)
def delete_user(user_id: int):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


# GROUPS


@app.post("/v1/groups/", response_model=dict)
def add_group(group: GroupCreate):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO groups (group_name) VALUES (?)", (group.group_name,))
        conn.commit()
        return {"message": "Group added successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Group name already exists")
#    finally:
#        conn.close()


@app.put("/v1/groups/{group_id}", response_model=dict)
def update_group(group_id: int, group: GroupUpdate):
    cursor = conn.cursor()

    updates = []
    params = []

    if group.group_name:
        updates.append("group_name = ?")
        params.append(group.group_name)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    params.append(group_id)

    query = f"UPDATE groups SET {', '.join(updates)} WHERE group_id = ?"

    cursor.execute(query, params)
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Group not found")

    return {"message": "Group updated successfully"}


@app.delete("/v1/groups/{group_id}", response_model=dict)
def delete_group(group_id: int):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM groups WHERE group_id = ?", (group_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Group not found")

    return {"message": "Group deleted successfully"}


# GROUP MEMBERSHIPS


@app.post("/v1/groups/{group_id}/memberships/", response_model=dict)
def add_user_to_group(group_id: int, membership: MembershipCreate):
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO group_memberships (group_id, user_id, role) VALUES (?, ?, ?)",
                       (group_id, membership.user_id, membership.role))
        conn.commit()
        return {"message": "User added to group successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User is already a member of the group")
#    finally:
#        conn.close()


@app.delete("/v1/groups/{group_id}/memberships/{user_id}", response_model=dict)
def remove_user_from_group(group_id: int, user_id: int):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM group_memberships WHERE group_id = ? AND user_id = ?", (group_id, user_id))
    conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Membership not found")

    return {"message": "User removed from group successfully"}

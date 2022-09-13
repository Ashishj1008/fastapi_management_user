from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from src.models import Record
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from schemas import db_helper
from schemas.db_helper import UserDetail, UpdateDetails
from src.database import SessionLocal, engine

app = FastAPI(
    title="user management", openapi_url="/openapi.json"
)

api_router = APIRouter()


def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@api_router.get("/")
def docs():
    return RedirectResponse(url="/docs")


# @api_router.get("/fetch", status_code=200)
# def get_user_details(db: Session = Depends(db_connection)) -> dict:
#     try:
#         cursor = db.execute("SELECT * FROM user_management_details").fetchall()
#         if cursor:
#             return {
#                 "status": 200,
#                 "message": "user details is available here",
#                 "payload": cursor
#             }
#         else:
#             return {
#                 "status": 404,
#                 "message": "user details is not available"
#             }
#     except Exception as e:
#         print("Error", e)
#         return {
#             "status": 500,
#             "message": "something went wrong."
#         }


@api_router.get("/fetch/")
def show_users(db: Session = Depends(db_connection)):
    try:
        records = db.query(Record).all()
        if records:
            return {
                "status": 201,
                "message": "users details available here",
                "payload": records
            }
        else:
            return {
                "status": 404,
                "message": "users details not found"
            }
    except Exception as e:
        print("Error", e)
        return {
            "status": 500,
            "message": "something went wrong."
        }


# @api_router.get("/fetch/{user_id}", status_code=200)
# def get_user_details(user_id: int, db: Session = Depends(db_connection)) -> dict:
#     try:
#         cursor = db.execute(f"SELECT * FROM user_management_details WHERE user_id={user_id}").fetchone()
#         if cursor:
#             return {
#                 "status": 200,
#                 "message": "user_details is available here by id values",
#                 "payload": cursor
#             }
#         else:
#             return {
#                 "status": 404,
#                 "message": "user_details is not available here"
#             }
#
#     except Exception as e:
#         print("Error", e)
#         return {
#             "status": 500,
#             "message": "something went wrong."
#         }

@api_router.get("/fetch/{user_id}")
def fetch_user_details(user_id: int):
    try:
        with Session(engine) as session:
            user = session.get(Record, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="user not found")
            return user

    except Exception as e:

        print("Error", e)
        return {
            "message": "something went wrong.",
            "payload": e
        }


# @api_router.post("/create", status_code=200)
# def create_item(data: UserDetail, db: Session = Depends(db_connection)) -> dict:
#     try:
#         db.execute(
#             f" INSERT INTO user_management_details(first_name, last_name, phone,email,dob,address) VALUES('{data.first_name}','{data.last_name}','{data.phone}','{data.email}','{data.dob}','{data.address}')")
#         db.commit()
#
#         return {
#
#             "status": 201,
#             "message": "user  created successfully",
#             "payload": {
#                 "first_name": data.first_name,
#                 "last_name": data.last_name,
#                 "phone": data.phone,
#                 "email": data.email,
#                 "address": data.address,
#                 "dob": data.dob
#             }
#         }
#
#     except Exception as e:
#         print("Error", e)
#         return {
#             "status": 500,
#             "message": "something went wrong."
#         }


@api_router.post("/create/")
def create_users(data: UserDetail):
    try:

        with Session(engine) as session:
            add_user_details = Record(first_name=data.first_name, last_name=data.last_name, phone=data.phone,
                                      email=data.email, address=data.address, dob=data.dob)
            session.add(add_user_details)
            session.commit()
            session.refresh(add_user_details)
            if add_user_details:
                return {
                    "status": 201,
                    "message": "user created successfully",
                    "payload": add_user_details}
            else:
                return {
                    "status": 404,
                    "message": "sorry user is not created successfully, kindly try again"
                }
    except Exception as e:

        print("Error", e)
        return {
            "status": 500,
            "message": "something went wrong."
        }


# @api_router.put("/update/{user_id}", status_code=200)
# def update_user(user_id: int, data: UserDetail, db: Session = Depends(db_connection)) -> dict:
#     try:
#         db.execute(
#             f"UPDATE user_management_details SET first_name='{data.first_name}',last_name='{data.last_name}', phone='{data.phone}', email='{data.email}', address='{data.address}', dob='{data.dob}' WHERE user_id={user_id};")
#         db.commit()
#         return {
#             "status": 200,
#             "message": "user details updated successfully",
#             "payload": data
#         }
#
#     except Exception as e:
#         print("Error", e)
#         return {
#             "status": 500,
#             "message": "something went wrong."
#         }


@api_router.put("/update/{user_id}")
def update_user(user_id: int, data: UpdateDetails):
    with Session(engine) as session:
        db_user = session.get(Record, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="user not found")
        user_data = data.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


# @api_router.delete("/delete/{user_id}", status_code=200)
# def delete_user(user_id: int, db: Session = Depends(db_connection)) -> dict:
#     try:
#         db.execute(f"DELETE FROM user_management_details WHERE user_id={user_id};")
#         db.commit()
#         return {
#             "status": 200,
#             "message": "user details deleted successfully",
#         }
#
#     except Exception as e:
#         print("Error", e)
#         return {
#             "status": 500,
#             "message": "something went wrong."
#         }


@api_router.delete("/delete/{user_id}")
def delete_user(user_id: int):
    try:
        with Session(engine) as session:
            user = session.get(Record, user_id)
            if user:
                session.delete(user)
                session.commit()
                return {"user is deleted successfully": True}
            raise HTTPException(status_code=404, detail="user not found")
    except Exception as e:
        print("Error", e)
        return {
            "message": "something went wrong.",
            "Error": e
        }


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

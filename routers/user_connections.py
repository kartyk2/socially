from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database_config import get_db
from config.log_config import Logger
from models import User, Connection
from datetime import datetime
from schemas.user_connection import ConnectionRequest, RespondToRequest, PendingRequestResponse
from commons.helper import get_current_user

connection_manager = APIRouter()

# Define loggers
error_logger = Logger.get_error_logger()
info_logger = Logger.get_api_info_logger()
success_logger = Logger.get_success_logger()

class UserConnection:
    def __init__(self, db: Session):
        self.db = db

    def send_connection_request(self, sender_id: UUID, receiver_id: UUID):
        try:
            # Check if the connection request already exists
            existing_request = self.db.query(Connection).filter(
                Connection.user_id == sender_id,
                Connection.connected_user_id == receiver_id
            ).first()

            if existing_request:
                if existing_request.status == "pending":
                    return {"message": "Connection request already sent."}
                else:
                    return {"message": "Connection request already processed."}

            new_request = Connection(
                user_id=sender_id,
                connected_user_id=receiver_id
            )
            self.db.add(new_request)
            self.db.commit()
            success_logger.info(f"Connection request sent from {sender_id} to {receiver_id}.")
            return {"message": "Connection request sent successfully."}
        except Exception as e:
            error_logger.error(f"Error while sending connection request from {sender_id} to {receiver_id}: {str(e)}")
            raise

    def find_pending_requests(self, user_id: UUID):
        try:
            pending_requests = self.db.query(Connection).filter(
                Connection.connected_user_id == user_id,
                Connection.status == "pending"
            ).all()
            return pending_requests
        except Exception as e:
            error_logger.error(f"Error while finding pending requests for user {user_id}: {str(e)}")
            raise

    def respond_to_request(self, request_id: UUID, response: str):
        try:
            connection = self.db.query(Connection).filter(Connection.id == request_id).first()
            if not connection:
                return {"message": "Request not found."}

            if response == "accept":
                connection.status = "accepted"
                success_logger.info(f"Connection request {request_id} accepted.")
            elif response == "reject":
                connection.status = "rejected"
                success_logger.info(f"Connection request {request_id} rejected.")
            else:
                return {"message": "Invalid response."}

            self.db.commit()
            return {"message": f"Connection request {response}ed successfully."}
        except Exception as e:
            error_logger.error(f"Error while responding to request {request_id}: {str(e)}")
            raise

@connection_manager.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@connection_manager.post('/send_request')
async def send_connection_request(connection_request: ConnectionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    connection_service = UserConnection(db)
    try:
        result = connection_service.send_connection_request(current_user.id, connection_request.receiver_id)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        error_logger.error(f"Failed to process connection request: {str(e)}")
        return JSONResponse(
            content="An internal error occurred while sending the connection request. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@connection_manager.get('/pending_requests', response_model=list[PendingRequestResponse])
async def find_pending_requests(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    connection_service = UserConnection(db)
    try:
        pending_requests = connection_service.find_pending_requests(current_user.id)
        return pending_requests
    except Exception as e:
        error_logger.error(f"Failed to fetch pending requests for user {current_user.id}: {str(e)}")
        return JSONResponse(
            content="An internal error occurred while retrieving pending requests. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@connection_manager.post('/respond_request')
async def respond_to_request(request_id: UUID, connection_response: RespondToRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    connection_service = UserConnection(db)
    try:
        result = connection_service.respond_to_request(request_id, connection_response.response)
        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        error_logger.error(f"Failed to respond to request {request_id}: {str(e)}")
        return JSONResponse(
            content="An internal error occurred while responding to the request. Please try again later.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.user import User, UserActivity
from models.connections import Connection, ConnectionStatus
from uuid import uuid4

from config.constants import get_settings

settinngs= get_settings()



# Database connection setup (replace with your actual database URL)
engine = create_engine(settinngs.pg_dsn.unicode_string())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_data_from_json(file_path: str):
    with open(file_path, 'r') as file:
        return json.load(file)

def insert_data(file_path: str):
    # Load the data from the JSON file
    data = load_data_from_json(file_path)
    
    # Create a new session
    session = SessionLocal()

    try:
        # Insert users
        user_map = {}  # To map usernames to user IDs
        for user_data in data["users"]:
            user = User(
                id=uuid4(),
                username=user_data["username"],
                name=user_data["name"],
                mobile=user_data["mobile"],
                email=user_data["email"],
                about=user_data["about"],
                joined=datetime.now()
            )
            session.add(user)
            user_map[user.username] = user.id  # Store the user ID for later use

            # Insert user activity
            user_activity = UserActivity(
                user_id=user.id,
                last_seen=datetime.now()
            )
            session.add(user_activity)

        # Commit the transaction
        session.commit()
        print("Data inserted successfully!")

    except Exception as e:
        session.rollback()
        print(f"Error occurred: {e}")
    finally:
        # Close the session
        session.close()

# Call the function to insert the data
insert_data('dummy_data.json')

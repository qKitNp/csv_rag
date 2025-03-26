from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pandas as pd
from typing import List, Dict
import motor.motor_asyncio

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'csv_database')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'csv_files')

# Initialize MongoDB client with Motor for async operations
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

class DocumentNotFoundError(Exception):
    pass

async def store_csv_document(file_path: str, file_id: str, file_name: str) -> None:
    """Store CSV file content in MongoDB as string"""
    try:
        # Read CSV file as string
        with open(file_path, 'r') as file:
            csv_content = file.read()
        
        # Create document structure
        document = {
            'file_id': file_id,
            'file_name': file_name,
            'content': csv_content
        }
        
        # Insert into MongoDB
        await collection.insert_one(document)
        
    except Exception as e:
        raise Exception(f"Error storing CSV document: {str(e)}")

async def get_all_files() -> List[Dict]:
    """Retrieve all file metadata including content"""
    try:
        # Include content in the projection
        cursor = collection.find({}, {'file_id': 1, 'file_name': 1, 'content': 1, '_id': 0})
        files = await cursor.to_list(length=None)
        # Return all fields including content
        return files
    except Exception as e:
        raise Exception(f"Error retrieving files: {str(e)}")

async def query_document(file_id: str, query: str) -> str:
    """Query a specific document"""
    try:
        document = await collection.find_one({'file_id': file_id})
        if not document:
            raise DocumentNotFoundError(f"Document with file_id {file_id} not found")
        
        # Convert the content back to DataFrame for querying
        df = pd.DataFrame(document['content'])
        
        # Execute the query using pandas eval
        # Note: This is a simple implementation. You might want to add more
        # sophisticated query handling based on your requirements
        try:
            result = df.query(query)
            return result.to_string()
        except Exception as e:
            return f"Query error: {str(e)}"
            
    except DocumentNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"Error querying document: {str(e)}")

async def delete_document(file_id: str) -> None:
    """Delete a document"""
    try:
        result = await collection.delete_one({'file_id': file_id})
        if result.deleted_count == 0:
            raise DocumentNotFoundError(f"Document with file_id {file_id} not found")
    except DocumentNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"Error deleting document: {str(e)}")

async def get_file_content(file_id: str) -> str:
    """Retrieve content of a specific file by ID"""
    try:
        # Find the document in MongoDB
        document = await collection.find_one({'file_id': file_id})
        if not document:
            raise DocumentNotFoundError(f"Document with file_id {file_id} not found")
        
        # Convert string content to DataFrame and back to formatted string
        try:
            # Use StringIO to parse CSV string
            from io import StringIO
            df = pd.read_csv(StringIO(document['content']))
            return df.to_string(index=False)
        except Exception as format_error:
            # Fallback to raw content if parsing fails
            # print(document['content'])
            return document['content']
            
    except DocumentNotFoundError:
        raise
    except Exception as e:
        raise Exception(f"Error retrieving file content: {str(e)}")
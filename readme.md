# CSV RAG API Server

A FastAPI server that enables uploading, querying, and managing CSV files using MongoDB for storage and Gemini AI for intelligent querying.

## Setup

1. Create a `.env` file with required environment variables:

```env
MONGO_URI=your_mongodb_connection_string
DB_NAME=csv_database
COLLECTION_NAME=csv_files
GEMINI_API_KEY=your_gemini_api_key
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --reload
```

## API Endpoints

### Upload CSV File

- **Endpoint**: `POST /upload`
- **Description**: Upload a CSV file to the server
- **Input**: CSV file (multipart/form-data)
- **Returns**: File ID and success message
- **Test in Swagger UI**:
  1. Navigate to `/docs`
  2. Expand POST /upload
  3. Click "Try it out"
  4. Upload CSV file
  5. Execute request

### List All Files

- **Endpoint**: `GET /files`
- **Description**: Retrieve all stored files
- **Returns**: List of files with IDs, names, and content
- **Test in Swagger UI**:
  1. Expand GET /files
  2. Click "Try it out"
  3. Execute request

### Query File Content

- **Endpoint**: `POST /query`
- **Description**: Query file content using Gemini AI
- **Input**:

```json
{
  "file_id": "your_file_id",
  "query": "What insights can you give me about this data?"
}
```

- **Returns**: AI-generated response about the data
- **Test in Swagger UI**:
  1. Expand POST /query
  2. Enter JSON payload
  3. Execute request

### Get File Content

- **Endpoint**: `GET /content/{file_id}`
- **Description**: Retrieve raw CSV file content
- **Input**: File ID (path parameter)
- **Returns**: CSV file content
- **Test in Swagger UI**:
  1. Expand GET /content/{file_id}
  2. Enter file ID
  3. Execute request

### Delete File

- **Endpoint**: `DELETE /file/{file_id}`
- **Description**: Remove a file from storage
- **Input**: File ID (path parameter)
- **Returns**: Success message
- **Test in Swagger UI**:
  1. Expand DELETE /file/{file_id}
  2. Enter file ID
  3. Execute request

## Error Handling

The API implements comprehensive error handling for:

- Invalid file formats (non-CSV)
- Missing files
- Database connection issues
- Query processing errors

All errors return appropriate HTTP status codes and descriptive messages.

## Testing with Swagger UI

1. Access Swagger UI at `http://localhost:8000/docs`
2. Test endpoints interactively
3. No authentication required
4. File IDs are UUID format
5. Save file IDs from upload responses for subsequent operations

## Technologies Used

- FastAPI
- MongoDB
- Google Gemini AI
- Python
- Swagger UI (OpenAPI)

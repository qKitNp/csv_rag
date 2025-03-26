import streamlit as st
import requests
import pandas as pd
from typing import Dict

# Configure the API endpoint
API_BASE_URL = "http://127.0.0.1:8000/"

def fetch_all_files() -> list:
    """Fetch all files from the API"""
    response = requests.get(f"{API_BASE_URL}/files")
    if response.status_code == 200:
        return response.json()
    return []

def get_file_content(file_id: str) -> Dict:
    """Get all content from a specific file"""
    response = requests.get(f"{API_BASE_URL}/content/{file_id}")
    if response.status_code == 200:
        return response.json()
    return {"response": "Error fetching file content"}

def main():
    st.title("CSV File Explorer")

    # Sidebar with file list
    st.sidebar.header("Available Files")
    files = fetch_all_files()
    
    # Store selected file ID in session state
    if "selected_file_id" not in st.session_state:
        st.session_state.selected_file_id = None
        st.session_state.selected_file_name = None

    # Create file selection buttons in sidebar
    for file in files:
        if st.sidebar.button(
            file["file_name"],
            key=file["file_id"],
            use_container_width=True,
            type="secondary" if file["file_id"] != st.session_state.selected_file_id else "primary"
        ):
            st.session_state.selected_file_id = file["file_id"]
            st.session_state.selected_file_name = file["file_name"]
            
    # Main content area
    if st.session_state.selected_file_id:
        st.subheader(f"Viewing: {st.session_state.selected_file_name}")
        
        # Fetch and display file content immediately
        result = get_file_content(st.session_state.selected_file_id)
        st.text("File Contents:")
        st.text(result["response"])
    else:
        st.info("Select a file from the sidebar to view its contents")

if __name__ == "__main__":
    main()
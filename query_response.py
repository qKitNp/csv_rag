from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from server_config import get_file_content
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Gemini model
llm = GoogleGenerativeAI(model="gemini-1.5-flash", 
                        google_api_key=os.getenv("GEMINI_API_KEY"))

# Create a prompt template
PROMPT_TEMPLATE = """
You are a helpful assistant that analyzes CSV data and answers questions about it.
Below is the content of a CSV file:

{csv_content}

Based on this data, please answer the following question:
{query}

Provide a clear and concise response based only on the data shown above.
"""

prompt = PromptTemplate(
    input_variables=["csv_content", "query"],
    template=PROMPT_TEMPLATE
)

async def generate_response(file_id: str, query: str) -> str:
    """
    Generate a response to a query about CSV content using LangChain and Gemini.
    
    Args:
        file_id (str): The ID of the CSV file in MongoDB
        query (str): The user's question about the data
        
    Returns:
        str: Generated response from the LLM
    """
    try:
        # Get the CSV content from MongoDB
        csv_content = await get_file_content(file_id)
        
        # Format the prompt with the CSV content and query
        formatted_prompt = prompt.format(
            csv_content=csv_content,
            query=query
        )
        
        # Generate response using the LLM
        response = llm.invoke(formatted_prompt)
        
        return response
        
    except Exception as e:
        return f"Error generating response: {str(e)}"
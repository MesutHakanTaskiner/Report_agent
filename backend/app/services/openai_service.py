import os
import json
from typing import List, Dict, Any, Optional
import base64
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from pypdf import PdfReader
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4o")

# List of fallback models in case the specified model is not available
FALLBACK_MODELS = ["gpt-4o", "gpt-3.5-turbo", "gpt-4"]

try:
    client = OpenAI(api_key=api_key)
    # Test if the client is working
    if api_key and api_key != "your_openai_api_key_here":
        print(f"OpenAI client initialized with model: {model_name}")
    else:
        print("Warning: OpenAI API key not set or using default value")
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    client = None

# Prompt templates for different analysis types
PROMPT_TEMPLATES = {
    "summarize": """
    You are an expert business analyst. Analyze the following data and provide a comprehensive summary:
    
    {file_content}
    
    Focus on the main points, key findings, and overall trends. Be concise but thorough.
    """,
    
    "trends": """
    You are an expert data analyst. Analyze the following data and identify key trends:
    
    {file_content}
    
    Focus on patterns over time, growth or decline in metrics, and any notable shifts or anomalies.
    Explain what these trends mean for the business.
    """,
    
    "kpis": """
    You are an expert business intelligence analyst. Extract and analyze the key performance indicators from the following data:
    
    {file_content}
    
    Identify the most important metrics, their current values, historical performance, and what they indicate about business health.
    Highlight any KPIs that require attention or show exceptional performance.
    """,
    
    "actions": """
    You are an expert business consultant. Based on the following data, generate actionable recommendations:
    
    {file_content}
    
    Provide specific, practical steps that can be taken to address issues or capitalize on opportunities.
    Prioritize your recommendations and explain the expected impact of each action.
    """,
    
    "compare": """
    You are an expert comparative analyst. Compare the information in the following data:
    
    {file_content}
    
    Identify similarities and differences, highlight strengths and weaknesses, and provide insights on what these comparisons reveal.
    Focus on meaningful comparisons that can drive business decisions.
    """
}

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file"""
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    text += "[Page contains no extractable text or images only]\n"
            
            if not text.strip():
                return "The PDF file does not contain any extractable text. It may contain only images or be scanned without OCR."
            
            return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_excel(file_path: str) -> str:
    """Extract text content from an Excel file"""
    try:
        # Try to read as Excel
        dfs = pd.read_excel(file_path, sheet_name=None)
        result = []
        
        for sheet_name, df in dfs.items():
            result.append(f"Sheet: {sheet_name}")
            result.append(df.to_string(index=True))
            result.append("\n")
        
        return "\n".join(result)
    except Exception as e:
        return f"Error extracting Excel content: {str(e)}"

def extract_text_from_csv(file_path: str) -> str:
    """Extract text content from a CSV file"""
    try:
        df = pd.read_csv(file_path)
        return df.to_string(index=True)
    except Exception as e:
        return f"Error extracting CSV content: {str(e)}"

def extract_file_content(file_path: str) -> str:
    """Extract content from a file based on its extension"""
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension in ['xlsx', 'xls']:
        return extract_text_from_excel(file_path)
    elif file_extension == 'csv':
        return extract_text_from_csv(file_path)
    else:
        # For text files or other formats, try to read as text
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # If not a text file, return a message
            return f"File format {file_extension} is not supported for direct text extraction."

async def analyze_files(file_paths: List[str], analysis_type: str = "summarize", user_message: str = "") -> str:
    """
    Analyze files using OpenAI API
    
    Args:
        file_paths: List of paths to files to analyze
        analysis_type: Type of analysis to perform (summarize, trends, kpis, actions, compare)
        user_message: Additional context or questions from the user
        
    Returns:
        Analysis result as a string
    """
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return "OpenAI API key is not configured. Please set your API key in the .env file."
    
    # Extract content from all files
    file_contents = []
    for file_path in file_paths:
        # Check if this is a dummy file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline()
            is_dummy = first_line.startswith("This is a dummy file for")
        except (UnicodeDecodeError, IOError):
            # If we can't read it as text, it's probably a binary file (like PDF)
            is_dummy = False
        
        if is_dummy:
            # This is a dummy file, create some sample content based on the filename
            file_name = os.path.basename(file_path).split('_', 1)[1]  # Remove the UUID prefix
            
            if file_name.lower().endswith('.pdf'):
                content = f"""Sample PDF content for {file_name}:
                
                Title: Business Report 2023
                
                Executive Summary:
                The company has shown strong growth in Q3 2023, with revenue increasing by 15% compared to the previous quarter. 
                Key performance indicators are trending positively, with customer acquisition costs decreasing by 10%.
                
                Financial Highlights:
                - Revenue: $10.5M (up 15% QoQ)
                - Gross Margin: 68% (up 3% QoQ)
                - Operating Expenses: $4.2M (down 5% QoQ)
                - Net Profit: $2.8M (up 22% QoQ)
                
                Market Analysis:
                The market share has increased to 23%, making us the second largest player in the industry.
                Competitor analysis shows that our product features are rated higher in 7 out of 10 categories.
                
                Recommendations:
                1. Increase marketing spend in the APAC region where we're seeing the highest growth
                2. Accelerate the development of the mobile application to capture the growing mobile user base
                3. Consider strategic partnerships with complementary service providers
                """
            elif file_name.lower().endswith(('.xlsx', '.xls')):
                content = f"""Sample Excel content for {file_name}:
                
                Sheet: Sales Data
                
                  Region  |  Q1 Sales  |  Q2 Sales  |  Q3 Sales  |  Q4 Sales  |  Total
                ----------|------------|------------|------------|------------|--------
                  North   |  $125,000  |  $142,000  |  $168,000  |  $182,000  | $617,000
                  South   |  $118,000  |  $126,000  |  $140,000  |  $152,000  | $536,000
                  East    |  $95,000   |  $102,000  |  $118,000  |  $125,000  | $440,000
                  West    |  $142,000  |  $156,000  |  $170,000  |  $188,000  | $656,000
                ----------|------------|------------|------------|------------|--------
                  Total   |  $480,000  |  $526,000  |  $596,000  |  $647,000  | $2,249,000
                
                Sheet: Product Performance
                
                  Product  |  Units Sold  |  Revenue  |  Profit Margin
                -----------|--------------|-----------|---------------
                  Product A|    12,500    |  $625,000 |     32%
                  Product B|    8,300     |  $415,000 |     28%
                  Product C|    15,200    |  $760,000 |     35%
                  Product D|    6,800     |  $340,000 |     40%
                """
            elif file_name.lower().endswith('.csv'):
                content = f"""Sample CSV content for {file_name}:
                
                Date,Customer,Product,Quantity,Price,Total
                2023-01-15,ABC Corp,Widget X,100,$25.00,$2500.00
                2023-01-22,XYZ Inc,Widget Y,50,$30.00,$1500.00
                2023-02-05,123 Industries,Widget Z,75,$22.50,$1687.50
                2023-02-18,ABC Corp,Widget X,150,$24.00,$3600.00
                2023-03-03,XYZ Inc,Widget Z,120,$22.00,$2640.00
                2023-03-17,123 Industries,Widget Y,80,$29.50,$2360.00
                2023-04-02,ABC Corp,Widget Z,200,$21.50,$4300.00
                2023-04-15,XYZ Inc,Widget X,100,$24.50,$2450.00
                """
            else:
                content = f"""Sample text content for {file_name}:
                
                This is a sample business document with some key information:
                
                - The project timeline has been extended by 2 weeks
                - Budget allocation has increased by 15%
                - Team size will grow from 8 to 12 members
                - New requirements include mobile support and API integration
                - Customer feedback shows 92% satisfaction rate
                """
        else:
            # This is a real file, extract its content
            content = extract_file_content(file_path)
        
        file_name = os.path.basename(file_path)
        file_contents.append(f"File: {file_name}\n\n{content}\n\n")
    
    combined_content = "\n".join(file_contents)
    
    # Get the appropriate prompt template
    prompt_template = PROMPT_TEMPLATES.get(analysis_type, PROMPT_TEMPLATES["summarize"])
    
    # Format the prompt with file content
    prompt = prompt_template.format(file_content=combined_content)
    
    # Add user message if provided
    if user_message:
        prompt += f"\n\nAdditional context from user: {user_message}"
    
    try:
        # Check if OpenAI client is initialized
        if not client:
            return "Error: OpenAI client not initialized. Please check your API key."
        
        # Try with the specified model first
        current_model = model_name
        print(f"Sending request to OpenAI API with model: {current_model}")
        print(f"Content length: {len(combined_content)} characters")
        
        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=current_model,
                messages=[
                    {"role": "system", "content": "You are an expert business analyst assistant that provides detailed, accurate, and insightful analysis of business data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
        except Exception as model_error:
            # If the specified model fails, try fallback models
            print(f"Error with model {current_model}: {str(model_error)}")
            
            for fallback_model in FALLBACK_MODELS:
                if fallback_model != current_model:
                    try:
                        print(f"Trying fallback model: {fallback_model}")
                        response = client.chat.completions.create(
                            model=fallback_model,
                            messages=[
                                {"role": "system", "content": "You are an expert business analyst assistant that provides detailed, accurate, and insightful analysis of business data."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3,
                            max_tokens=2000
                        )
                        print(f"Successfully used fallback model: {fallback_model}")
                        break
                    except Exception as fallback_error:
                        print(f"Error with fallback model {fallback_model}: {str(fallback_error)}")
                        continue
            else:
                # If all models fail, raise the original error
                raise model_error
        
        # Return the response
        result = response.choices[0].message.content
        print(f"Received response from OpenAI API: {len(result)} characters")
        return result
    except Exception as e:
        error_message = str(e)
        print(f"Error calling OpenAI API: {error_message}")
        
        # Check for common errors
        if "API key" in error_message:
            return "Error: Invalid OpenAI API key. Please check your API key in the .env file."
        elif "model" in error_message:
            return f"Error: The model '{model_name}' is not available. Please check your OPENAI_MODEL setting in the .env file."
        elif "too many tokens" in error_message or "maximum context length" in error_message:
            return "Error: The file content is too large for the AI model to process. Please try with a smaller file or extract the most important parts."
        else:
            return f"Error analyzing files: {error_message}"

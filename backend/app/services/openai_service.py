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
    """
    Extract text content and metadata from a PDF file
    
    This function extracts text from each page of a PDF file, handles pages with
    no extractable text, and attempts to extract metadata when available.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            
            # Extract metadata if available
            metadata = []
            info = reader.metadata
            if info:
                if info.title:
                    metadata.append(f"Title: {info.title}")
                if info.author:
                    metadata.append(f"Author: {info.author}")
                if info.creator:
                    metadata.append(f"Creator: {info.creator}")
                if info.creation_date:
                    metadata.append(f"Creation Date: {info.creation_date}")
            
            # Check if PDF is encrypted
            if reader.is_encrypted:
                return "This PDF file is encrypted and cannot be processed without a password."
            
            # Extract text from pages
            text_content = []
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"--- Page {i+1} ---\n{page_text}")
                else:
                    text_content.append(f"--- Page {i+1} ---\n[Page contains no extractable text or images only]")
            
            # Combine metadata and content
            result = []
            if metadata:
                result.append("PDF METADATA:")
                result.extend(metadata)
                result.append("\nPDF CONTENT:")
            
            result.extend(text_content)
            
            final_text = "\n".join(result)
            
            if not any(page.extract_text() for page in reader.pages):
                final_text += "\n\nNote: This PDF file does not contain any extractable text. It may contain only images or be scanned without OCR."
            
            return final_text
    except Exception as e:
        error_msg = str(e)
        print(f"Error extracting text from PDF {file_path}: {error_msg}")
        
        if "password" in error_msg.lower():
            return "This PDF file is encrypted and requires a password to access."
        elif "not a PDF" in error_msg.lower():
            return "The file does not appear to be a valid PDF document."
        else:
            return f"Error extracting text from PDF: {error_msg}"

def extract_text_from_excel(file_path: str) -> str:
    """
    Extract text content from an Excel file with improved formatting and metadata
    
    This function extracts data from all sheets in an Excel file, preserves formatting
    where possible, and includes sheet statistics and structure information.
    """
    try:
        # Try to read as Excel
        dfs = pd.read_excel(file_path, sheet_name=None)
        result = []
        
        # Add file metadata
        result.append(f"EXCEL FILE: {os.path.basename(file_path)}")
        result.append(f"Total Sheets: {len(dfs)}")
        result.append("")
        
        # Process each sheet
        for sheet_name, df in dfs.items():
            # Add sheet header with statistics
            result.append(f"SHEET: {sheet_name}")
            result.append(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Check for empty dataframe
            if df.empty:
                result.append("This sheet is empty.")
                result.append("")
                continue
            
            # Add column types information
            result.append("Column Types:")
            for col, dtype in df.dtypes.items():
                result.append(f"  - {col}: {dtype}")
            
            # Add data preview with better formatting
            result.append("\nData Preview:")
            
            # Format the dataframe for better readability
            # Handle large dataframes by showing head and tail
            if len(df) > 20:
                preview = pd.concat([df.head(10), df.tail(10)])
                result.append(preview.to_string(index=True))
                result.append(f"\n[...{len(df) - 20} more rows not shown...]")
            else:
                result.append(df.to_string(index=True))
            
            # Add basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                result.append("\nNumeric Column Statistics:")
                stats = df[numeric_cols].describe().to_string()
                result.append(stats)
            
            result.append("\n" + "-" * 50 + "\n")
        
        return "\n".join(result)
    except Exception as e:
        error_msg = str(e)
        print(f"Error extracting Excel content from {file_path}: {error_msg}")
        
        if "No engine for filetype" in error_msg:
            return "This file is not a valid Excel file or is in an unsupported format."
        elif "read permission" in error_msg.lower():
            return "Cannot access the Excel file. It may be locked or you don't have permission to read it."
        else:
            return f"Error extracting Excel content: {error_msg}"

def extract_text_from_csv(file_path: str) -> str:
    """
    Extract text content from a CSV file with improved formatting and analysis
    
    This function attempts to intelligently parse CSV files with different delimiters
    and encodings, and provides formatted output with data statistics.
    """
    try:
        # Try to detect encoding
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        df = None
        detected_encoding = None
        
        # Try different encodings
        for encoding in encodings:
            try:
                # First try to detect delimiter
                with open(file_path, 'r', encoding=encoding) as f:
                    sample = f.read(4096)
                
                # Count potential delimiters in the sample
                delimiters = [',', ';', '\t', '|']
                delimiter_counts = {d: sample.count(d) for d in delimiters}
                likely_delimiter = max(delimiter_counts, key=delimiter_counts.get)
                
                # Try to read with the detected delimiter
                df = pd.read_csv(file_path, encoding=encoding, delimiter=likely_delimiter)
                detected_encoding = encoding
                break
            except Exception:
                continue
        
        # If all attempts failed, try pandas default behavior
        if df is None:
            df = pd.read_csv(file_path)
            detected_encoding = 'unknown (pandas default)'
        
        # Build the result
        result = []
        result.append(f"CSV FILE: {os.path.basename(file_path)}")
        result.append(f"Detected Encoding: {detected_encoding}")
        result.append(f"Dimensions: {df.shape[0]} rows × {df.shape[1]} columns")
        
        # Add column information
        result.append("\nColumn Names:")
        for i, col in enumerate(df.columns):
            result.append(f"  {i+1}. {col}")
        
        # Add data types
        result.append("\nColumn Types:")
        for col, dtype in df.dtypes.items():
            result.append(f"  - {col}: {dtype}")
        
        # Add data preview
        result.append("\nData Preview:")
        
        # Format the dataframe for better readability
        # Handle large dataframes by showing head and tail
        if len(df) > 20:
            preview = pd.concat([df.head(10), df.tail(10)])
            result.append(preview.to_string(index=True))
            result.append(f"\n[...{len(df) - 20} more rows not shown...]")
        else:
            result.append(df.to_string(index=True))
        
        # Add basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            result.append("\nNumeric Column Statistics:")
            stats = df[numeric_cols].describe().to_string()
            result.append(stats)
        
        # Check for missing values
        missing = df.isnull().sum()
        if missing.sum() > 0:
            result.append("\nMissing Values:")
            for col, count in missing.items():
                if count > 0:
                    result.append(f"  - {col}: {count} missing values ({count/len(df):.1%})")
        
        return "\n".join(result)
    except Exception as e:
        error_msg = str(e)
        print(f"Error extracting CSV content from {file_path}: {error_msg}")
        
        if "No such file" in error_msg:
            return f"The CSV file {os.path.basename(file_path)} does not exist."
        elif "Expecting" in error_msg and "delimiter" in error_msg:
            return "The CSV file has an unexpected format or delimiter. Please check the file format."
        else:
            return f"Error extracting CSV content: {error_msg}"

def extract_file_content(file_path: str) -> str:
    """
    Extract content from a file based on its extension with enhanced detection and handling
    
    This function intelligently detects file types, handles various formats, and provides
    appropriate extraction methods with improved error handling and formatting.
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    
    # Get file size
    try:
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Warn about very large files
        if file_size_mb > 50:
            print(f"Warning: Processing a large file ({file_size_mb:.1f} MB). This may take some time.")
    except Exception as e:
        print(f"Warning: Could not determine file size: {str(e)}")
    
    # Get file extension and try to determine file type
    file_name = os.path.basename(file_path)
    file_extension = file_path.split('.')[-1].lower() if '.' in file_path else ''
    
    # Add file metadata to output
    result_header = [
        f"FILE: {file_name}",
        f"Size: {os.path.getsize(file_path) / 1024:.1f} KB",
        f"Last Modified: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')}",
        f"Type: {file_extension.upper() if file_extension else 'Unknown'}"
    ]
    
    # Process based on file extension
    if file_extension == 'pdf':
        content = extract_text_from_pdf(file_path)
    elif file_extension in ['xlsx', 'xls']:
        content = extract_text_from_excel(file_path)
    elif file_extension == 'csv':
        content = extract_text_from_csv(file_path)
    elif file_extension in ['json', 'jsonl']:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                content = json.dumps(data, indent=2)
                result_header.append(f"JSON Structure: {type(data).__name__}")
                if isinstance(data, dict):
                    result_header.append(f"Top-level keys: {len(data)}")
                elif isinstance(data, list):
                    result_header.append(f"Array length: {len(data)}")
        except json.JSONDecodeError:
            # Try as JSONL (one JSON object per line)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    sample = []
                    for i, line in enumerate(lines[:10]):  # Process first 10 lines
                        try:
                            obj = json.loads(line.strip())
                            sample.append(obj)
                        except:
                            pass
                    
                    content = f"JSONL file with {len(lines)} lines\n\nSample of first {min(10, len(lines))} lines (parsed):\n"
                    content += json.dumps(sample, indent=2)
            except Exception as e:
                content = f"Error parsing JSON/JSONL file: {str(e)}"
    elif file_extension in ['txt', 'md', 'py', 'js', 'html', 'css', 'java', 'c', 'cpp', 'h', 'hpp', 'xml', 'yaml', 'yml']:
        # Handle text files with encoding detection
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    result_header.append(f"Encoding: {encoding}")
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            content = "Could not decode the file with any of the attempted encodings."
    else:
        # For unknown formats, try to detect if it's text or binary
        try:
            with open(file_path, 'rb') as file:
                sample = file.read(1024)
                # Check if the sample contains null bytes (common in binary files)
                if b'\x00' in sample:
                    content = f"Binary file detected. File format {file_extension if file_extension else 'unknown'} is not supported for direct text extraction."
                else:
                    # Try to decode as text
                    try:
                        with open(file_path, 'r', encoding='utf-8') as text_file:
                            content = text_file.read()
                            result_header.append("Note: File appears to be text despite unknown extension")
                    except UnicodeDecodeError:
                        content = f"File appears to be binary. Format {file_extension if file_extension else 'unknown'} is not supported for direct text extraction."
        except Exception as e:
            content = f"Error reading file: {str(e)}"
    
    # Combine header and content
    return "\n".join(result_header) + "\n\n" + content

async def generate_conversation_response(conversation_history: List[Dict[str, str]], user_message: str) -> str:
    """
    Generate a response to a user message based on conversation history
    
    Args:
        conversation_history: List of previous messages in the conversation
        user_message: The current user message to respond to
        
    Returns:
        Assistant's response as a string
    """
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        return "OpenAI API key is not configured. Please set your API key in the .env file."
    
    try:
        # Check if OpenAI client is initialized
        if not client:
            return "Error: OpenAI client not initialized. Please check your API key."
        
        # Prepare messages for the API call
        messages = [
            {"role": "system", "content": "You are an expert business analyst assistant that provides helpful, detailed, and accurate responses to user questions. You can analyze business data, provide insights, and answer general questions."}
        ]
        
        # Add conversation history (limited to last 10 messages to avoid token limits)
        for msg in conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        # Try with the specified model first
        current_model = model_name
        print(f"Sending request to OpenAI API with model: {current_model}")
        
        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model=current_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
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
                            messages=messages,
                            temperature=0.7,
                            max_tokens=1000
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
            return "Error: The conversation is too long for the AI model to process. Some context may be lost."
        else:
            return f"Error generating response: {error_message}"

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

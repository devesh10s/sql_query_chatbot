# import requests
# import psycopg2
# import csv
# import json
# import os
# from contextlib import closing
# import openai

# prompts = [{"role": "system", "content":"Generate an SQL query based on the following metadata and user input."},]

# # Structure to hold table-column mappings
# class OsqueryTable:
#     def __init__(self, table):
#         self.table = table
#         self.columns = []

# # Function to load osquery table metadata from a file
# def load_metadata(filename):
#     metadata = {}
#     with open(filename, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip header if present
#         for line in reader:
#             if len(line) == 2:  # Ensure valid table-column pairs
#                 table, column = line
#                 if table not in metadata:
#                     metadata[table] = OsqueryTable(table)
#                 metadata[table].columns.append(column)
#             else:
#                 print(f"Skipping invalid line: {line}")
#     return metadata

# # Function to call OpenAI API and get SQL query
# def call_openai(user_input, metadata):
#     api_key = "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"  # API Key directly in the code
#     if not api_key:
#         print("OpenAI API key is missing!")
#         return "ERROR"

#     url = "https://api.openai.com/v1/completions"
#     prompt = "Generate an SQL query based on the following metadata and user input:\n"

#     # Add metadata to the prompt
#     max_metadata_entries = 5
#     for table, data in list(metadata.items())[:max_metadata_entries]:
#         prompt += f"Table: {table}, Columns: {' '.join(data.columns)}\n"

#     # Sanitize the user input
#     sanitized_input = user_input.replace('\n', ' ')

#     prompt += f"User Input: {sanitized_input}\nSQL Query:"

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }

#     post_data = {
#         "model": "text-davinci-003",
#         "prompt": prompt,
#         "max_tokens": 100
#     }

#     response = requests.post(url, headers=headers, json=post_data)
    
#     if response.status_code != 200:
#         print(f"Request failed with status code {response.status_code}")
#         return "ERROR"

#     response_data = response.json()
#     try:
#         if 'choices' in response_data and response_data['choices']:
#             sql_query = response_data['choices'][0]['text']
#             print(f"Generated SQL Query: {sql_query}")
#             return sql_query
#         else:
#             print("Invalid response format or no SQL query found.")
#             return "ERROR"
#     except KeyError:
#         print(f"Error parsing OpenAI response: {response_data}")
#         return "ERROR"

# # Function to execute SQL query on PostgreSQL
# def execute_query(query):
#     try:
#         with closing(psycopg2.connect(dbname="fleet", user="vajra", password="admin", host="localhost")) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(query)
#                 result = cur.fetchall()
#                 print("Query Result:")
#                 for row in result:
#                     print("\t".join(str(field) for field in row))
#     except Exception as e:
#         print(f"Database error: {e}")

# # Main chatbot function
# def chatbot(metadata):
#     print("Welcome to AI-powered osquery chatbot! Type 'exit' to quit.")

#     while True:
#         user_input = input("\nYou: ")
        
#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break
#         elif user_input:
#             prompts.append({"role": "user", "content": user_input})

#             ai_response = call_openai(prompts, metadata)
#         if ai_response != "ERROR":
#             execute_query(ai_response)

# # Main function
# def main():
#     metadata_file = "/home/devesh/VajraServer/sql_chatbot/table_schemas.csv"
#     metadata = load_metadata(metadata_file)
#     chatbot(metadata)

# if __name__ == "__main__":
#     main()

# import requests
# import csv
# import openai
# import google.generativeai as genai
# genai.configure(api_key="AIzaSyAhU32fpgem_08Cuk3KzIYQWbnvG6GOjWI")
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Explain how AI works")
# print(response.text)

# # Initialize prompts
# prompts = [{"role": "system", "content": "Generate an SQL query based on the following metadata and user input."}]

# # Class to hold table-column mappings
# class OsqueryTable:
#     def __init__(self, table):
#         self.table = table
#         self.columns = []

# # Function to load osquery table metadata from a CSV file
# def load_metadata(filename):
#     metadata = {}
#     try:
#         with open(filename, 'r') as file:
#             reader = csv.reader(file)
#             for line in reader:
#                 if len(line) == 2:  # Ensure valid table-column pairs
#                     table, column = line
#                     if table not in metadata:
#                         metadata[table] = OsqueryTable(table)
#                     metadata[table].columns.append(column)
#                 else:
#                     print(f"Skipping invalid line: {line}")
#     except FileNotFoundError:
#         print(f"Metadata file not found: {filename}")
#     return metadata

# # Function to call OpenAI API and generate an SQL query
# def call_openai(prompts):
#     api_key = "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"  # API Key directly in the code
#     if not api_key:
#         print("OpenAI API key is missing!")
#         return "ERROR"

#     openai.api_key = api_key
#     # usage = openai.Usage.retrieve()
#     # print(usage)

#     # Prepare messages for chat completion
#     messages = [
#         {"role": "system", "content": "Generate an SQL query based on the following metadata and user input."}
#     ]
#     messages.extend(prompts)
#     print(messages)  # Add the user's prompts

#     try:
#         # Call the ChatCompletion API
#         response = openai.Completion.create(
#             model="gpt-3.5-turbo",  # Use this model if `gpt-4` is not available
#             prompt=[
#                 {"role": "system", "content": messages[0]['content']},])
#         print(response.choices[0].message['content']) # Print the generated SQL query

#         # Extract the response content
#         sql_query = response.choices[0].message['content'].strip()
#         return sql_query

#     except openai.OpenAIError as e:  # Use the correct exception class
#         print(f"OpenAI API error: {e}")
#         return "ERROR"

# # Main chatbot function
# def chatbot(metadata):
#     print("Welcome to the AI-powered osquery chatbot! Type 'exit' to quit.")
    
#     # Add metadata to prompts
#     meta_info = "\n".join([f"Table: {table}, Columns: {', '.join(data.columns)}" for table, data in metadata.items()])
#     prompts.append({"role": "system", "content": f"Metadata:\n{meta_info}"})
    
#     while True:
#         user_input = input("\nYou: ")

#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break
#         elif user_input.strip():
#             # Add user input to prompts
#             prompts.append({"role": "user", "content": user_input})

#             # Call OpenAI to get SQL query
#             ai_response = call_openai(prompts)
            
#             if ai_response != "ERROR":
#                 print(f"\nGenerated SQL Query:\n{ai_response}")
#                 # Add AI's response back to the conversation context
#                 prompts.append({"role": "assistant", "content": ai_response})
#             else:
#                 print("Failed to generate an SQL query. Please try again.")

# # Main function
# def main():
#     metadata_file = "/home/devesh/VajraServer/sql_chatbot/table_schemas.csv"
#     metadata = load_metadata(metadata_file)

#     if metadata:
#         chatbot(metadata)
#     else:
#         print("Failed to load metadata. Please check the file and try again.")

# if __name__ == "__main__":
#     main()
# import requests
# import csv
# import openai

# # Class to hold table-column mappings
# class OsqueryTable:
#     def __init__(self, table):
#         self.table = table
#         self.columns = []

# # Function to load osquery table metadata from a CSV file
# def load_metadata(filename):
#     metadata = {}
#     try:
#         with open(filename, 'r') as file:
#             reader = csv.reader(file)
#             for line in reader:
#                 if len(line) == 2:  # Ensure valid table-column pairs
#                     table, column = line
#                     if table not in metadata:
#                         metadata[table] = OsqueryTable(table)
#                     metadata[table].columns.append(column)
#                 else:
#                     print(f"Skipping invalid line: {line}")
#     except FileNotFoundError:
#         print(f"Metadata file not found: {filename}")
#     return metadata

# # Function to call OpenAI API and generate an SQL query
# def call_openai(prompts):
#     api_key = "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"  # Use your actual API key
#     if not api_key:
#         print("OpenAI API key is missing!")
#         return "ERROR"

#     openai.api_key = api_key

#     try:
#         # Call the ChatCompletion API
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # Use this model if `gpt-4` is not available
#             messages=prompts  # Use the dynamic messages list
#         )
        
#         # Extract the response content
#         sql_query = response['choices'][0]['message']['content'].strip()
#         return sql_query

#     except openai.OpenAIError as e:  # Use the correct exception class
#         print(f"OpenAI API error: {e}")
#         return "ERROR"

# # Main chatbot function
# def chatbot(metadata):
#     print("Welcome to the AI-powered osquery chatbot! Type 'exit' to quit.")
    
#     # Prepare metadata string to add to the prompt
#     meta_info = "\n".join([f"Table: {table}, Columns: {', '.join(data.columns)}" for table, data in metadata.items()])
    
#     # Start the conversation with the system message for metadata
#     prompts = [
#         {"role": "system", "content": "Generate an SQL query based on the following metadata and user input."},
#         {"role": "system", "content": f"Metadata:\n{meta_info}"}
#     ]
    
#     while True:
#         user_input = input("\nYou: ")

#         if user_input.lower() == "exit":
#             print("Goodbye!")
#             break
#         elif user_input.strip():
#             # Add user input to prompts
#             prompts.append({"role": "user", "content": user_input})

#             # Call OpenAI to get SQL query
#             ai_response = call_openai(prompts)
            
#             if ai_response != "ERROR":
#                 print(f"\nGenerated SQL Query:\n{ai_response}")
#                 # Add AI's response back to the conversation context
#                 prompts.append({"role": "assistant", "content": ai_response})
#             else:
#                 print("Failed to generate an SQL query. Please try again.")

# # Main function
# def main():
#     metadata_file = "/home/devesh/VajraServer/sql_chatbot/table_schemas.csv" # Provide the correct path to your metadata file
#     metadata = load_metadata(metadata_file)

#     if metadata:
#         chatbot(metadata)
#     else:
#         print("Failed to load metadata. Please check the file and try again.")

# if __name__ == "__main__":
#     main()

import csv
import google.generativeai as genai

# Configure the Google Generative AI client with your API key
genai.configure(api_key="AIzaSyAhU32fpgem_08Cuk3KzIYQWbnvG6GOjWI")

# Class to hold table-column mappings
class OsqueryTable:
    def __init__(self, table):
        self.table = table
        self.columns = []

# Function to load osquery table metadata from a CSV file
def load_metadata(filename):
    metadata = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for line in reader:
                if len(line) == 2:  # Ensure valid table-column pairs
                    table, column = line
                    if table not in metadata:
                        metadata[table] = OsqueryTable(table)
                    metadata[table].columns.append(column)
                else:
                    print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print(f"Metadata file not found: {filename}")
    return metadata

# Function to call Google Generative AI and generate an SQL query
def call_genai(prompts):
    try:
        # Combine all prompts into a single string input for genai
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in prompts])
        
        # Call the Generative AI API
        model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Explain how AI works")
        response = model.generate_content(context)
        
        # Extract the response content
        sql_query = response.text.strip()
        return sql_query

    except Exception as e:
        print(f"Google Generative AI error: {e}")
        return "ERROR"

# Main chatbot function
def chatbot(metadata):
    print("Welcome to the AI-powered osquery chatbot! Type 'exit' to quit.")
    
    # Prepare metadata string to add to the prompt
    meta_info = "\n".join([f"Table: {table}, Columns: {', '.join(data.columns)}" for table, data in metadata.items()])
    
    # Start the conversation with the system message for metadata
    prompts = [
        {"role": "system", "content": "Generate an SQL query based on the following metadata and user input."},
        {"role": "system", "content": f"Metadata:\n{meta_info}"}
    ]
    
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.strip():
            # Add user input to prompts
            prompts.append({"role": "user", "content": user_input})

            # Call Google Generative AI to get SQL query
            ai_response = call_genai(prompts)
            
            if ai_response != "ERROR":
                print(f"\nGenerated SQL Query:\n{ai_response}")
                # Add AI's response back to the conversation context
                prompts.append({"role": "assistant", "content": ai_response})
            else:
                print("Failed to generate an SQL query. Please try again.")

# Main function
def main():
    metadata_file = "/home/devesh/VajraServer/sql_chatbot/table_schemas.csv"  # Provide the correct path to your metadata file
    metadata = load_metadata(metadata_file)

    if metadata:
        chatbot(metadata)
    else:
        print("Failed to load metadata. Please check the file and try again.")

if __name__ == "__main__":
    main()

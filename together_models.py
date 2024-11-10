import os
import json
import re
from together import Together

# Initialize Together client
client = Together()

def generate_description(content):
    # Define the system prompt for summarization
    # system_prompt = """
    # You are summarizing the content of a web page. Focus on key services, features, or information while keeping the description clear, informative, and brief.
    
    # - Summarize the main points like services or important details.
    # - Avoid irrelevant content.
    # - Keep the description under 150 words.
    # - Ensure clarity and neutrality.
    # """
    system_prompt = """
    Extract the following from the web page:
    1. An appropriate title for the page based on its content.
    2. A list of actions or services a user can perform on the page, including:
    - Any forms the user can fill out and their purpose.
    - Any data processing details or steps mentioned.
    - Any options the user can select.

    Output in the following JSON format:
    {
        "title": "Appropriate Title Here",
        "actions": [
            "Action 1",
            "Action 2",
            ...
        ]
    }
    """

    # Send the content to the Together API to generate a summary
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
    )

    # Extract and return the generated description from the response
    return response.choices[0].message.content

def extract_url(content):
    # Extract the URL from the content (assumes URL is present in the content text)
    match = re.search(r'https?://[^\s]+', content)
    if match:
        return match.group(0)
    return None

# Directory path with .txt files
directory = "./formatted_files"
checkpoint_file = "checkpoint.txt"
description_directory = "./descriptions"

# Load last processed file from checkpoint
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as f:
        last_processed = f.read().strip()
        if not last_processed:
            last_processed = None
else:
    last_processed = None

# Optional: Set an upper limit on the number of files to process
max_files_to_process = 5
files_processed = 0

# Process files, starting from the checkpoint
resume_processing = last_processed is None
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt"):
        # Check if processing should resume and limit files if max is set
        if resume_processing or filename == last_processed:
            resume_processing = True
            file_path = os.path.join(directory, filename)

            # Read file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            try:
                # Extract URL from the content
                url = extract_url(content)
                if not url:
                    print(f"URL not found in {filename}. Skipping...")
                    continue

                # Generate description using the Together API
                description = generate_description(content)
                
                # Create a dictionary to save as JSON
                result = {
                    "link": url,
                    "description": description
                }
                
                # Save the result to a new file with the same name
                new_filename = os.path.splitext(filename)[0] + "_description.json"
                new_filepath = os.path.join(description_directory, new_filename)
                
                with open(new_filepath, 'w', encoding='utf-8') as json_file:
                    json.dump(result, json_file, ensure_ascii=False, indent=4)
                
                print(f"Description for {filename} saved as {new_filename}\n")
                
                # Update checkpoint after successful processing
                with open(checkpoint_file, "w") as f:
                    f.write(filename)

                files_processed += 1
                if files_processed >= max_files_to_process:
                    print("Reached the maximum file processing limit.")
                    break
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                break

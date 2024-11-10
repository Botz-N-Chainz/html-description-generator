import os
import requests

# API endpoint for Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {
    "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"
}

def generate_description(content):
    # Prepare the data for the API request
    payload = {
        "inputs": f"Summarize the services offered in the following page: {content}",
        "parameters": {
            "max_length": 150,
            "temperature": 0.7
        }
    }

    # Send the request to the API
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Extract the generated description from the response
        output = response.json()
        return output[0]["generated_text"]
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Directory path with .txt files
directory = "./formatted_files"
checkpoint_file = "checkpoint.txt"

# Load last processed file from checkpoint
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, "r") as f:
        last_processed = f.read().strip()
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
                # Generate description using the API
                description = generate_description(content)
                print(f"Description for {filename}:\n{description}\n")
                
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

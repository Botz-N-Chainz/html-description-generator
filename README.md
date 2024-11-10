# HTML to Info Converter

This project is designed to convert HTML content into structured information using machine learning models. It processes text files containing HTML content, extracts relevant information, and generates descriptions in JSON format.

## Features

- Extracts titles and actions from web pages.
- Utilizes machine learning models for content analysis.
- Supports checkpointing to resume processing from the last file.
- Outputs results in JSON format.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/html-to-info-converter.git
   cd html-to-info-converter
   ```

2. **Create and Activate a Virtual Environment**

   On Windows, using Git Bash:

   ```bash
   python -m venv myenv
   source myenv/Scripts/activate
   ```

3. **Install Dependencies**
   You will have to pre-install the requirements.txt file in your environment (Hehe).

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**

   Ensure you have the necessary API keys set as environment variables (may be different for each model):

   ```bash
   export TOGETHER_API_KEY=your_together_api_key
   export HUGGINGFACE_API_KEY=your_huggingface_api_key
   export OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. **Prepare Input Files**

   Place your `.txt` files containing HTML content in the `formatted_files` directory.

2. **Run the Script Using OpenAI API**

   Execute the main script to process the files using the OpenAI API with the `gpt-4o-mini` model:

   ```bash
   python generator-openai.py
   ```

   This will generate descriptions and save them in the `descriptions` directory.

3. **Run the Script Using Hugging Face API**

   If you are using the Hugging Face API with the `Mistral-7B-Instruct-v0.3` model, run the following script:

   ```bash
   python description_generate.py
   ```

   Ensure that the script is configured to use the appropriate API endpoints and authentication details.

## Code Overview

- **`generator-openai.py`**: Main script for processing files and generating descriptions using the OpenAI API with the `gpt-4o-mini` model.
  - Initializes the OpenAI client and processes files from the `formatted_files` directory.
  - Generates descriptions using the OpenAI API.
  - Saves results in JSON format.
- **`together_models.py`**: Main script for processing files and generating descriptions using the Together API with the `meta-llama/Meta-Llama-3-8B-Instruct-Lite` model.

  - Initializes the Together client and processes files from the `formatted_files` directory.
  - Generates descriptions using the Together API.
  - Saves results in JSON format.

- **`description_generate.py`**: Script for processing files using the Hugging Face API with the `Mistral-7B-Instruct-v0.3` model.
  - Sends requests to the Hugging Face Inference API.
  - Processes and outputs results in JSON format.

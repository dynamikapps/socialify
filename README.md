# Socialify

Socialify is a Python-based web application designed to automate the generation of social media content from blog posts. It uses AI models to create engaging captions for multiple social media platforms.

## Features

- Scrape blog posts from a given website URL.
- Generate a summary of each blog post.
- Generate social media captions for each blog post.
- Output the generated content to a CSV file.
- Option to include the blog post URL and summary in the output file.
- Option to generate a separate output file for each social media platform.

## Prerequisites

- Python 3.9 or higher
- Conda package manager

## Installation

1. Clone this repository to your local machine.

2. Create a new conda environment:

```bash
conda create --name socialify python=3.9
```

3. Activate the conda environment:

```bash
conda activate socialify
```

4. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

5. Set up your API keys and other sensitive data in the .env file and secrets.toml file.

## Usage

1. Ensure you have activated the conda environment:

```bash
conda activate socialify
```

2. Run the application:

```bash
streamlit run main.py
```

3. Open your web browser and navigate to http://localhost:8501.

4. Enter your website URL and select the blog posts you want to generate content for.

5. Select the social media platforms you want to generate content for.

6. Check the options to include the blog post URL and summary in the output file, and to generate a separate file for each platform, if desired.

7. Click the "Generate Content" button to generate the social media content.

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## License
This project is licensed under the terms of the MIT license.

## Contact
For any inquiries or feedback, please contact handy@dynamikapps.com

## Video Explainer

For a detailed walkthrough of the application, check out our [YouTube Video Explainer](https://youtu.be/W8yoKxtnhqw).
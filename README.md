# Semantic Web Integration Project

This project is an enhanced tool developed for the Semantic Web class at the Hellenic Mediterranean University. It's designed to read and process SPARQL queries, utilizing the OpenAI API to apply advanced AI models for data analysis and insights within the realm of semantic web technologies.

## Features

- Efficient handling of SPARQL queries from various file formats.
- Integration with OpenAI API for leveraging AI in semantic web contexts.
- Utilization of pandas for robust data manipulation and analysis.

## Installation

1. Clone the project repository.

```bash
git clone <repository-url>
```

2. Install the necessary Python dependencies.

```bash
pip install -r requirements.txt
```

Please ensure `requirements.txt` includes `openai`, `pandas`, and any other dependencies your project might use.

3. Set up your OpenAI API key in `main.py` by replacing `Replace with your OpenAI API Key` with your actual key.

## Usage

Execute the project with:

```bash
python main.py --log_file_path <path-to-your-sparql-query-file>
```

Ensure your SPARQL query file is prepared according to the project's expectations.

## Contributions

We encourage contributions! Fork the project, make your changes, and submit a pull request.

## License

This project is under the MIT License. See the LICENSE file for full details.
# GrowAgent Webpage to Markdown Converter

Part of the GrowAgent application, this module crawls webpages, converts them to markdown, and stores them in an S3 bucket. It also finds and processes any linked documents (PDF, Excel, Word, CSV) and converts them to markdown as well.

## Project Structure

```
growagent-app/
├── frontend/          # React frontend application
├── backend/           # Backend API server
└── scripts/          # Webpage processing scripts
    ├── __init__.py
    ├── webpage_to_markdown.py
    ├── document_processor.py
    └── requirements.txt
```

## Features

- Converts webpages to markdown format
- Detects and processes linked documents:
  - PDF files
  - Excel files (.xls, .xlsx)
  - Word documents (.doc, .docx)
  - CSV files
- Stores all markdown files in an S3 bucket
- Handles relative and absolute URLs
- Maintains document structure and formatting

## Prerequisites

1. Python 3.8 or higher
2. Pandoc (for document conversion)
   ```bash
   # macOS
   brew install pandoc
   
   # Ubuntu/Debian
   sudo apt-get install pandoc
   
   # Windows
   choco install pandoc
   ```
3. AWS credentials configured with S3 access
4. crawl4ai package installed from the repository

## Installation

1. Navigate to the scripts directory:
   ```bash
   cd growagent-app/scripts
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up AWS credentials:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_REGION=your_region  # defaults to us-east-1
   ```

## Usage

Basic usage:
```bash
python webpage_to_markdown.py <url> <s3_bucket>
```

Example:
```bash
python webpage_to_markdown.py https://example.com my-markdown-bucket
```

Options:
- `--skip-docs`: Skip processing of linked documents

## Output Structure

The script organizes files in the S3 bucket as follows:

```
s3://your-bucket/
├── pages/
│   └── domain.com_path_to_page.md
└── documents/
    ├── domain.com_path_to_document1.md
    └── domain.com_path_to_document2.md
```

## Using as a Module

You can also use the functionality programmatically:

```python
from growagent_app.scripts import process_webpage

async def convert_page():
    await process_webpage("https://example.com", "my-bucket")
```

## Error Handling

- The script logs all operations and errors to the console
- Failed document conversions are reported but don't stop the overall process
- Network errors and conversion failures are handled gracefully

## Limitations

- PDF conversion requires Pandoc to be installed
- Some complex document formatting may not be preserved
- Excel files are converted to markdown tables, which may not be suitable for very large spreadsheets
- Password-protected documents are not supported

## Development

To contribute to this module:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/growagent-app.git
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   pytest scripts/tests/
   ```

4. Format code:
   ```bash
   black scripts/
   flake8 scripts/
   mypy scripts/

# CreepyCrawly

A modern web crawling application that converts webpages to markdown and stores them in S3. Built with FastAPI, React, and Redis.

## 🏗 Architecture

The application consists of three main components:

- **Frontend**: React + Vite application providing a user interface for crawl configuration and status monitoring
- **Backend**: FastAPI service handling crawl requests and webpage processing
- **Redis**: Cache and queue management for crawl operations

## 🚀 Features

- Web crawling with configurable parameters
- Automatic conversion of webpages to markdown
- Document processing and conversion:
  - PDF to markdown conversion
  - Word documents (.doc, .docx) to markdown
  - Excel spreadsheets (.xls, .xlsx) to markdown tables
  - CSV files to markdown tables
- Recursive document discovery and processing
- Configurable crawling parameters
- S3 storage integration for all converted content
- Real-time crawl status monitoring
- Docker containerization for easy deployment

## 📄 Document Processing

The application provides comprehensive document processing capabilities:

### Webpage Processing
- Converts webpage content to clean, structured markdown
- Extracts and processes all linked documents
- Maintains document structure and formatting
- Handles relative and absolute URLs

### Document Conversion
- **PDF Processing**: Converts PDF documents while preserving text formatting
- **Word Documents**: Processes .doc and .docx files maintaining document structure
- **Spreadsheets**: Converts Excel and CSV files into markdown tables
- **Batch Processing**: Handles multiple documents from a single webpage

### Storage & Version Control
- **Flexible Storage Options**:
  - Local filesystem storage (default)
  - S3 storage (optional)
- **Organized Directory Structure**:
  - `/website/` - Converted webpage content (local storage)
  - `/documents/` - Processed document files (local storage)
  - Or equivalent paths in S3 when configured
- **Storage Features**:
  - Automatic directory creation
  - Clear naming convention based on source URLs
  - Automatic content-type setting
  - Fallback to local storage if S3 is not configured

### Change Detection & Versioning
- **Smart Crawling**: Implements content versioning to avoid reprocessing unchanged content
- **Multiple Hash Strategies**:
  - Content Hash: Detects any changes in the actual content
  - Structural Hash: Identifies structural changes while ignoring minor content updates
- **Configurable Behavior**:
  - Enable/disable change detection
  - Force refresh option for complete recrawls
  - Customizable change detection strategy
- **Version History**:
  - Tracks all content versions with timestamps
  - Maintains crawl history with detailed metadata
  - Documents processing status and changes

## 🛠 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Pandoc (required for document conversion)
  ```bash
  # macOS
  brew install pandoc
   
  # Ubuntu/Debian
  sudo apt-get install pandoc
   
  # Windows
  choco install pandoc
  ```

### Optional Dependencies

- AWS Account with S3 access (optional - local storage is used by default)
- OpenAI API key (optional - only needed for LLM-powered features)
- Ollama (optional - can be used instead of OpenAI for local LLM features)

The core web crawling and markdown conversion features work without any API keys or external services. API keys are only required for optional enhanced features:
- OpenAI API key: For LLM-powered content extraction and filtering
- AWS credentials: For S3 storage (local storage is used by default)

## ⚡️ Quick Start

1. Install Pandoc (required for document conversion):
   ```bash
   # macOS
   brew install pandoc
   
   # Ubuntu/Debian
   sudo apt-get install pandoc
   
   # Windows
   choco install pandoc
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CreepyCrawly.git
   cd CreepyCrawly
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration. By default, local storage is used. If you want to use S3 storage:
   ```bash
   # Enable S3 storage (optional)
   CRAWL_USE_S3=true
   
   # Configure AWS credentials if using S3
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=your_region
   S3_BUCKET=your_bucket_name
   ```

4. Start the application:
   ```bash
   docker-compose up
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Development Setup

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python src/main.py
```

### Scripts

```bash
cd scripts
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## 📦 Project Structure

```
.
├── frontend/               # React + Vite frontend application
│   ├── src/               # Frontend source code
│   └── Dockerfile         # Frontend container configuration
├── backend/               # FastAPI backend service
│   ├── src/              # Backend source code
│   │   ├── main.py       # Main application entry
│   │   └── routes/       # API route definitions
│   └── Dockerfile        # Backend container configuration
├── scripts/              # Utility scripts for webpage processing
├── docker-compose.yml    # Multi-container Docker configuration
└── README.md            # This file
```

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| AWS_ACCESS_KEY_ID | AWS access key | Required |
| AWS_SECRET_ACCESS_KEY | AWS secret key | Required |
| AWS_REGION | AWS region | us-east-1 |
| S3_BUCKET | S3 bucket for markdown storage | my-markdown-bucket |
| VITE_API_URL | Backend API URL | http://backend:8000 |

### Database Configuration

The application supports both SQLite (default) and PostgreSQL databases. Configure using these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| CRAWL_DB_TYPE | Database type ('sqlite' or 'postgres') | sqlite |
| CRAWL_DB_HOST | PostgreSQL host | - |
| CRAWL_DB_PORT | PostgreSQL port | 5432 |
| CRAWL_DB_NAME | Database name | crawlai.db |
| CRAWL_DB_USER | PostgreSQL username | - |
| CRAWL_DB_PASSWORD | PostgreSQL password | - |

For SQLite, only `CRAWL_DB_TYPE` and `CRAWL_DB_NAME` are required. For PostgreSQL, all fields must be configured.

## 🐳 Docker Configuration

The application uses Docker Compose to manage three services:

1. **frontend**: React application (port 5173)
2. **backend**: FastAPI service (port 8000)
3. **redis**: Redis instance (port 6379)

Each service is configured with appropriate volumes and environment variables for development and production use.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

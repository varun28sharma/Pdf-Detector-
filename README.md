# PDF Integrity Analyzer

A powerful tool for analyzing PDF files to detect modifications, verify integrity, and identify potential tampering. This tool performs comprehensive analysis including metadata inspection, digital signature verification, content integrity checks, and OCR-based analysis for scanned documents.


## Features

- **Metadata Analysis**: Extracts and analyzes PDF metadata for inconsistencies
- **Digital Signature Verification**: Checks for and validates digital signatures
- **Content Integrity**: Performs structural analysis and content verification
- **OCR Capabilities**: Detects and analyzes scanned documents
- **Hash Verification**: Generates SHA-256 hashes for file integrity checking
- **Suspicious Pattern Detection**: Identifies potential signs of tampering

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR engine installed on your system
- Poppler (required for pdf2image)

### Installing Tesseract OCR

#### Windows
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Add Tesseract to your system PATH

#### Linux
```bash
sudo apt-get install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

### Installing Poppler

#### Windows
1. Download from: http://blog.alivate.com.au/poppler-windows/
2. Add to your system PATH

#### Linux
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd pdf-integrity-analyzer
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
python pdf_analyzer.py path/to/your/document.pdf
```

### Python API

```python
from pdf_analyzer import analyze_pdf

# Analyze a PDF file
report = analyze_pdf("path/to/your/document.pdf")

# Access the analysis results
print(report)
```

## Analysis Components

### 1. File Information
- File size
- MIME type
- SHA-256 hash

### 2. Metadata Analysis
- Title, author, subject, keywords
- Creation and modification dates
- Creator and producer information
- Suspicious pattern detection

### 3. Digital Signature Analysis
- Presence of digital signatures
- Signature details and validation
- Signature location in document

### 4. Content Integrity
- Page count
- Text content analysis
- Scanned document detection
- Structure verification

## Output Format

The tool generates a JSON report containing:
```json
{
    "file_info": {
        "path": "path/to/file.pdf",
        "size": 1234567,
        "mime_type": "application/pdf",
        "hash": "sha256_hash_value"
    },
    "metadata_analysis": {
        "title": "Document Title",
        "author": "Author Name",
        "creation_date": "2023-01-01T00:00:00",
        "modification_date": "2023-01-01T00:00:00",
        "suspicious_patterns": []
    },
    "signature_analysis": {
        "has_signatures": true,
        "signature_count": 1,
        "signatures": [...]
    },
    "content_analysis": {
        "page_count": 10,
        "is_scanned": false,
        "content_analysis": [...]
    },
    "timestamp": "2023-01-01T00:00:00"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

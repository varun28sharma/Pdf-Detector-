import os
import hashlib
import mimetypes
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from PyPDF2 import PdfReader
from dateutil.parser import parse
import json
import re

class PDFIntegrityAnalyzer:
    def __init__(self, pdf_path: str):
        """Initialize the PDF analyzer with the path to the PDF file."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF")
            
        try:
            self.pdf_path = pdf_path
            self.reader = PdfReader(pdf_path)
            self.file_size = os.path.getsize(pdf_path)
            self.original_hash = None  # Store original hash for comparison
        except Exception as e:
            raise ValueError(f"Failed to initialize PDF reader: {str(e)}")
    
    def calculate_file_hash(self) -> str:
        """Calculate SHA-256 hash of the entire PDF file."""
        try:
            sha256_hash = hashlib.sha256()
            with open(self.pdf_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"Error calculating hash: {str(e)}"
    
    def parse_pdf_date(self, date_str: str) -> Optional[datetime]:
        """Parse PDF date format (D:YYYYMMDDHHMMSS+HH'MM')."""
        try:
            # Remove 'D:' prefix if present
            if date_str.startswith('D:'):
                date_str = date_str[2:]
            
            # Extract the main date part (YYYYMMDDHHMMSS)
            match = re.match(r'(\d{14})', date_str)
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, '%Y%m%d%H%M%S')
            return None
        except:
            return None
    
    def check_metadata_consistency(self) -> List[str]:
        """Check metadata for signs of modification."""
        issues = []
        try:
            metadata = self.reader.metadata
            if not metadata:
                issues.append("No metadata found - potential sign of tampering")
                return issues
            
            # Check creation and modification dates
            creation_date = metadata.get("/CreationDate", "")
            mod_date = metadata.get("/ModDate", "")
            
            if not creation_date:
                issues.append("Missing creation date")
            if not mod_date:
                issues.append("Missing modification date")
            
            if creation_date and mod_date:
                c_date = self.parse_pdf_date(creation_date)
                m_date = self.parse_pdf_date(mod_date)
                
                if c_date and m_date:
                    if m_date < c_date:
                        issues.append("Modification date is before creation date - likely tampered")
                    if m_date > datetime.now():
                        issues.append("Future modification date detected - likely tampered")
                else:
                    issues.append("Invalid date format in metadata - potential tampering")
            
            # Check for common PDF editor signatures
            producer = metadata.get("/Producer", "").lower()
            creator = metadata.get("/Creator", "").lower()
            suspicious_tools = ["acrobat", "adobe", "pdf editor", "pdf tool"]
            for tool in suspicious_tools:
                if tool in producer or tool in creator:
                    issues.append(f"Document modified with {tool}")
                    
        except Exception as e:
            issues.append(f"Error analyzing metadata: {str(e)}")
        
        return issues
    
    def check_permissions(self) -> Dict:
        """Check PDF permissions and encryption."""
        try:
            is_encrypted = self.reader.is_encrypted
            permissions = {}
            
            if is_encrypted:
                permissions["is_encrypted"] = True
                try:
                    # Try to decrypt with empty password
                    self.reader.decrypt("")
                    permissions["encryption_status"] = "Encrypted but accessible"
                except:
                    permissions["encryption_status"] = "Encrypted and locked"
            else:
                permissions["is_encrypted"] = False
                permissions["encryption_status"] = "Not encrypted"
            
            return permissions
        except Exception as e:
            return {"error": f"Failed to check permissions: {str(e)}"}
    
    def analyze_integrity(self, original_hash: str = None) -> Dict:
        """Analyze PDF integrity and check for modifications."""
        current_hash = self.calculate_file_hash()
        
        # Store hash if this is the first analysis
        if original_hash:
            self.original_hash = original_hash
        elif not self.original_hash:
            self.original_hash = current_hash
        
        issues = self.check_metadata_consistency()
        permissions = self.check_permissions()
        
        is_modified = False
        if self.original_hash and current_hash != self.original_hash:
            is_modified = True
        
        result = {
            "is_original": not is_modified and not issues,
            "hash": current_hash,
            "permissions": permissions,
            "issues_found": issues
        }
        
        # Simplified output for easy understanding
        if result["is_original"]:
            print("TRUE - Document is original")
        else:
            print("FAKE - Document has been modified")
            print("\nDetails:")
            if is_modified:
                print("- Hash mismatch detected")
            for issue in issues:
                print(f"- {issue}")
            print("\nPermissions:")
            for perm, value in permissions.items():
                print(f"- {perm}: {value}")
        
        return result

def analyze_pdf(pdf_path: str, original_hash: str = None) -> Dict:
    """Analyze a PDF file for integrity."""
    try:
        analyzer = PDFIntegrityAnalyzer(pdf_path)
        return analyzer.analyze_integrity(original_hash)
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python pdf_analyzer.py <path_to_pdf> [original_hash]")
        print("Example: python pdf_analyzer.py document.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    original_hash = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        analyze_pdf(pdf_path, original_hash)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1) 
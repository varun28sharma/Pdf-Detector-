import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os
import tempfile

def detect_screenshot(pdf_path):
    """
    Analyze PDF pages to detect if they are screenshots.
    Returns a percentage indicating likelihood of being a screenshot.
    """
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        
        if not images:
            return {"error": "Could not convert PDF to images"}
        
        total_score = 0
        total_pages = len(images)
        
        for img in images:
            # Convert PIL image to OpenCV format
            img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            
            # Calculate edge density
            edges = cv2.Canny(gray, 100, 200)
            edge_density = np.count_nonzero(edges) / edges.size
            
            # Calculate noise level
            noise = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate compression artifacts
            dct = cv2.dct(np.float32(gray))
            dct_compressed = np.zeros_like(dct)
            dct_compressed[:8, :8] = dct[:8, :8]
            idct = cv2.idct(dct_compressed)
            compression_artifacts = np.mean(np.abs(gray - idct))
            
            # Calculate screenshot probability based on features
            score = 0
            
            # High edge density often indicates text/screenshots
            if edge_density > 0.1:
                score += 30
            
            # Low noise often indicates screenshots
            if noise < 100:
                score += 20
            
            # Compression artifacts often present in screenshots
            if compression_artifacts > 5:
                score += 20
            
            # Check for uniform color regions (common in UI screenshots)
            color_std = np.std(img_cv, axis=(0,1))
            if np.mean(color_std) < 30:
                score += 30
            
            total_score += score
        
        # Calculate final percentage
        screenshot_probability = (total_score / total_pages) / 100.0
        
        return {
            "is_screenshot": screenshot_probability > 0.5,
            "probability": round(screenshot_probability * 100, 2),
            "total_pages": total_pages
        }
        
    except Exception as e:
        return {"error": f"Error analyzing PDF: {str(e)}"} 
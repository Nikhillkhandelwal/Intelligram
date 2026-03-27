import os
import sys
from waitress import serve
from app_main import app

if __name__ == '__main__':
    # Ensure we are in the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    port = int(os.environ.get('PORT', 8080))
    print(f"🚀 IntelliGram Production Server starting on http://localhost:{port}")
    print("Serving frontend from: ../frontend/dist")
    print("API Endpoints active: /analyze, /trend, /niche, /explore, /deep_analysis, /recommend, /competitor")
    
    try:
        serve(app, host='0.0.0.0', port=port, threads=6)
    except Exception as e:
        print(f"❌ Server Error: {e}")

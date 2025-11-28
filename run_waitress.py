import os
import sys
from waitress import serve
from logistica_SV.wsgi import application

def main():
    # Add the project directory to the sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    port = os.getenv('PORT', '8000')
    print(f"--- Logistica SV Production Server ---")
    print(f"Serving on http://localhost:{port}")
    print(f"Press Ctrl+C to stop.")
    
    serve(application, host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()

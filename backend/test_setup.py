"""
Test script to verify backend setup
Run this after installing dependencies to ensure everything works
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing Python package imports...")
    
    packages = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'flask_socketio': 'Flask-SocketIO',
        'openai': 'OpenAI',
        'dotenv': 'python-dotenv'
    }
    
    failed = []
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            failed.append(name)
    
    return len(failed) == 0, failed

def test_env():
    """Test if .env file exists"""
    print("\nTesting environment configuration...")
    
    import os
    from pathlib import Path
    
    env_file = Path('.env')
    if env_file.exists():
        print("  ✓ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your-openai-api-key-here':
            print("  ✓ OPENAI_API_KEY is set")
            return True
        else:
            print("  ✗ OPENAI_API_KEY not configured")
            print("    Please edit .env and add your OpenAI API key")
            return False
    else:
        print("  ✗ .env file not found")
        print("    Please copy .env.example to .env")
        return False

def test_openai_connection():
    """Test OpenAI API connection"""
    print("\nTesting OpenAI API connection...")
    
    try:
        import os
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'your-openai-api-key-here':
            print("  ⚠ Skipping (API key not configured)")
            return True
        
        client = OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("  ✓ OpenAI API connection successful")
        return True
        
    except Exception as e:
        print(f"  ✗ OpenAI API connection failed: {str(e)}")
        return False

def main():
    print("=" * 50)
    print("MedCall Backend Setup Verification")
    print("=" * 50)
    print()
    
    # Test imports
    imports_ok, failed = test_imports()
    
    if not imports_ok:
        print("\n❌ Some packages are missing. Please run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Test environment
    env_ok = test_env()
    
    # Test OpenAI (optional)
    if env_ok:
        api_ok = test_openai_connection()
    else:
        api_ok = False
    
    print("\n" + "=" * 50)
    if imports_ok and env_ok:
        print("✅ Backend setup verified!")
        print("\nYou can now run: python app.py")
        if not api_ok:
            print("\n⚠️  Note: OpenAI API test was skipped or failed.")
            print("   The app will work once you configure a valid API key.")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
    print("=" * 50)

if __name__ == '__main__':
    main()

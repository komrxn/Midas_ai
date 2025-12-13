#!/usr/bin/env python3
"""
Quick setup script for AI Accountant API.
Creates .env file from template and generates sample data.
"""
import os
import secrets
from pathlib import Path


def main():
    print("🚀 AI Accountant API - Quick Setup\n")
    
    # Check if .env exists
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
    else:
        print("📝 Creating .env file from template...")
        
        # Generate secure secret key
        secret_key = secrets.token_urlsafe(32)
        
        # Read template
        with open(".env.example", "r") as f:
            template = f.read()
        
        # Replace secret key
        env_content = template.replace(
            "SECRET_KEY=your-secret-key-change-in-production-min-32-chars",
            f"SECRET_KEY={secret_key}"
        )
        
        # Write .env
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ .env file created!")
        print(f"   Generated SECRET_KEY: {secret_key[:20]}...")
        print("\n⚠️  IMPORTANT: Update these values in .env:")
        print("   - DATABASE_URL (PostgreSQL connection)")
        print("   - OPENAI_API_KEY (from OpenAI dashboard)")
    
    print("\n" + "="*50)
    print("📋 Next Steps:")
    print("="*50)
    print("\n1. Create PostgreSQL database:")
    print("   createdb accountant_db")
    print("\n2. Run database schema:")
    print("   psql -U postgres -d accountant_db -f schema.sql")
    print("\n3. (Optional) Generate and load sample data:")
    print("   python -m api.utils.sample_data")
    print("   psql -U postgres -d accountant_db -f sample_data.sql")
    print("\n4. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n5. Start the server:")
    print("   uvicorn api.main:app --reload")
    print("\n6. Visit API docs:")
    print("   http://localhost:8000/docs")
    print("\n" + "="*50)


if __name__ == "__main__":
    main()

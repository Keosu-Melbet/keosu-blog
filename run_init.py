#!/usr/bin/env python3
"""
Quick script to initialize the Kèo Sư database with sample data
Run this after first setup to populate the database
"""

import subprocess
import sys
import os

def main():
    """Run the initialization script"""
    print("🏈 Kèo Sư Database Initialization")
    print("=" * 40)
    
    # Check if init_data.py exists
    if not os.path.exists('init_data.py'):
        print("❌ init_data.py not found!")
        sys.exit(1)
    
    try:
        # Run the initialization script
        print("🚀 Starting database initialization...")
        result = subprocess.run([sys.executable, 'init_data.py'], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Database initialization completed successfully!")
            print("\n📄 Output:")
            print(result.stdout)
            
            print("\n🌐 Next steps:")
            print("   1. Run: python main.py")
            print("   2. Visit: http://localhost:5000")
            print("   3. Enjoy your Kèo Sư website!")
            
        else:
            print("❌ Database initialization failed!")
            print("\n🔍 Error details:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Failed to run initialization: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

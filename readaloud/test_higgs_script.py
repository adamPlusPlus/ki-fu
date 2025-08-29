#!/usr/bin/env python3
"""
Test script to check Higgs Audio script functionality
"""
import os
import sys
import subprocess

def test_higgs_script():
    """Test if Higgs Audio script exists and what arguments it expects"""
    
    # Check Higgs Audio path
    higgs_path = "H:/AI/higgs/higgs-audio"
    script_path = os.path.join(higgs_path, "examples", "generation.py")
    
    print(f"🔍 Testing Higgs Audio script...")
    print(f"📁 Path: {higgs_path}")
    print(f"📜 Script: {script_path}")
    
    if not os.path.exists(higgs_path):
        print("❌ Higgs Audio directory not found!")
        return False
    
    if not os.path.exists(script_path):
        print("❌ Generation script not found!")
        print("📋 Available files in examples:")
        try:
            examples_dir = os.path.join(higgs_path, "examples")
            if os.path.exists(examples_dir):
                for file in os.listdir(examples_dir):
                    print(f"   - {file}")
        except Exception as e:
            print(f"   Error listing examples: {e}")
        return False
    
    print("✅ Generation script found!")
    
    # Try to get help from the script
    try:
        print("\n🔧 Testing script help...")
        result = subprocess.run(
            [sys.executable, script_path, "--help"],
            capture_output=True,
            text=True,
            cwd=higgs_path,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Script help command successful!")
            print("📋 Available arguments:")
            print(result.stdout)
        else:
            print("⚠️ Script help command failed, but script exists")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Script help command timed out")
    except Exception as e:
        print(f"❌ Error testing script: {e}")
    
    # Try to run with minimal arguments
    try:
        print("\n🧪 Testing minimal script execution...")
        result = subprocess.run(
            [sys.executable, script_path, "--version"],
            capture_output=True,
            text=True,
            cwd=higgs_path,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Script version command successful!")
            print(f"Output: {result.stdout.strip()}")
        else:
            print("⚠️ Script version command failed")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Script version command timed out")
    except Exception as e:
        print(f"❌ Error testing script: {e}")
    
    return True

if __name__ == "__main__":
    test_higgs_script()

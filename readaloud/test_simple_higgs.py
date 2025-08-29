#!/usr/bin/env python3
"""
Simple test for Higgs Audio without subprocess timeout
"""

import os
import sys
import subprocess

def test_higgs_direct():
    """Test Higgs Audio directly"""
    print("🔧 Testing Higgs Audio directly...")
    
    # Change to Higgs Audio directory
    higgs_dir = "H:/AI/higgs/higgs-audio"
    if not os.path.exists(higgs_dir):
        print(f"❌ Higgs Audio not found at: {higgs_dir}")
        return False
    
    os.chdir(higgs_dir)
    print(f"📁 Changed to directory: {os.getcwd()}")
    
    # Test with a simple command
    test_text = "Hello, this is a test of the ReadAloud system."
    output_file = "test_simple.wav"
    
    cmd = [
        "python",
        "examples/generation.py",
        "--transcript", test_text,
        "--out_path", output_file,
        "--temperature", "0.3"
    ]
    
    print(f"🚀 Running command: {' '.join(cmd)}")
    print(f"⏱️  This may take 1-2 minutes on first run...")
    
    try:
        # Run without timeout first
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=higgs_dir
        )
        
        print(f"✅ Command completed!")
        print(f"   Return code: {result.returncode}")
        
        if result.stdout:
            print(f"   Stdout: {result.stdout[-500:]}")  # Last 500 chars
        
        if result.stderr:
            print(f"   Stderr: {result.stderr[-500:]}")  # Last 500 chars
        
        if result.returncode == 0 and os.path.exists(output_file):
            print(f"🎉 Audio generated successfully: {output_file}")
            file_size = os.path.getsize(output_file)
            print(f"   File size: {file_size} bytes")
            return True
        else:
            print(f"❌ Generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_higgs_direct()
    if success:
        print("\n🎯 Higgs Audio is working! The issue might be in the subprocess handling.")
    else:
        print("\n💥 Higgs Audio test failed.")
    
    input("\nPress Enter to continue...")

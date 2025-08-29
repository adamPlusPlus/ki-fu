#!/usr/bin/env python3
"""
Simple test script for ReadAloud functionality
"""
import os
import sys
import subprocess
import json

def test_config():
    """Test if configuration file exists and is valid"""
    try:
        with open('readaloud_config.json', 'r') as f:
            config = json.load(f)
        print("✓ Configuration file loaded successfully")
        print(f"  TTS Engine: {config.get('tts_engine', 'Not set')}")
        print(f"  Higgs Path: {config.get('higgs_config', {}).get('model_path', 'Not set')}")
        return config
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return None

def test_higgs_audio():
    """Test if Higgs Audio is accessible"""
    try:
        higgs_path = "H:/AI/higgs/higgs-audio"
        if os.path.exists(higgs_path):
            print(f"✓ Higgs Audio directory found: {higgs_path}")
            
            # Check for key files
            generation_script = os.path.join(higgs_path, "examples", "generation.py")
            if os.path.exists(generation_script):
                print(f"✓ Generation script found: {generation_script}")
            else:
                print(f"⚠ Generation script not found")
                
            return True
        else:
            print(f"✗ Higgs Audio directory not found: {higgs_path}")
            return False
    except Exception as e:
        print(f"✗ Error checking Higgs Audio: {e}")
        return False

def test_python_dependencies():
    """Test if required Python packages are available"""
    required_packages = ['torch', 'torchaudio', 'transformers', 'accelerate']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} available")
        except ImportError:
            print(f"✗ {package} not available")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠ Missing packages: {', '.join(missing_packages)}")
        print("  Run: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✓ All required packages available")
        return True

def test_streamdeck_actions():
    """Test if StreamDeck action files exist"""
    action_files = [
        "streamdeck/actions/read_clipboard.bat",
        "streamdeck/actions/read_selection.bat", 
        "streamdeck/actions/stop_audio.bat",
        "streamdeck/actions/read_file.bat"
    ]
    
    all_exist = True
    for action_file in action_files:
        if os.path.exists(action_file):
            print(f"✓ {action_file} exists")
        else:
            print(f"✗ {action_file} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 ReadAloud System Test")
    print("=" * 40)
    
    # Test configuration
    config = test_config()
    print()
    
    # Test Higgs Audio
    higgs_ok = test_higgs_audio()
    print()
    
    # Test Python dependencies
    deps_ok = test_python_dependencies()
    print()
    
    # Test StreamDeck actions
    actions_ok = test_streamdeck_actions()
    print()
    
    # Summary
    print("=" * 40)
    print("📊 Test Summary:")
    
    if config and higgs_ok and deps_ok and actions_ok:
        print("🎉 All tests passed! ReadAloud is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Set up StreamDeck buttons pointing to the .bat files")
        print("2. Test with: python test_simple.py")
        print("3. Try reading clipboard: Copy text, then press StreamDeck button")
    else:
        print("⚠ Some tests failed. Please fix the issues above.")
        
        if not higgs_ok:
            print("\n🔧 To fix Higgs Audio:")
            print("   Run: setup_higgs.bat")
            
        if not deps_ok:
            print("\n🔧 To fix dependencies:")
            print("   Run: pip install torch torchaudio transformers accelerate")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to verify the TimesFM frontend is working correctly.
"""

import requests
import time
import subprocess
import sys

def test_frontend_availability():
    """Test if the frontend is accessible."""
    print("🔍 Testing TimesFM Frontend Availability")
    print("-" * 40)
    
    try:
        # Test if the frontend is running
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running and accessible")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Frontend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running or not accessible")
        print("   Make sure to run: streamlit run timesfm_frontend.py")
        return False
    except Exception as e:
        print(f"❌ Error testing frontend: {e}")
        return False

def test_streamlit_process():
    """Test if Streamlit process is running."""
    print("\n🔍 Testing Streamlit Process")
    print("-" * 40)
    
    try:
        # Check if streamlit process is running
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True
        )
        
        if "streamlit" in result.stdout:
            print("✅ Streamlit process is running")
            lines = [line for line in result.stdout.split('\n') if 'streamlit' in line]
            for line in lines[:3]:  # Show first 3 processes
                print(f"   {line}")
            return True
        else:
            print("❌ Streamlit process not found")
            return False
    except Exception as e:
        print(f"❌ Error checking processes: {e}")
        return False

def main():
    """Run all frontend tests."""
    print("🌾 TimesFM Frontend Test Suite")
    print("=" * 50)
    
    # Test 1: Check if frontend is accessible
    frontend_ok = test_frontend_availability()
    
    # Test 2: Check if streamlit process is running
    process_ok = test_streamlit_process()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("-" * 40)
    print(f"Frontend Accessibility: {'✅ PASS' if frontend_ok else '❌ FAIL'}")
    print(f"Streamlit Process: {'✅ PASS' if process_ok else '❌ FAIL'}")
    
    if frontend_ok and process_ok:
        print("\n🎉 All tests passed! Frontend is working correctly.")
        print("\n🌐 Access your TimesFM frontend at:")
        print("   http://localhost:8501")
        print("\n📋 Available features:")
        print("   • Interactive forecasting dashboard")
        print("   • Multiple agricultural data types")
        print("   • CSV file upload support")
        print("   • Real-time visualization")
        print("   • Download forecast results")
        return True
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        print("\n🔧 To start the frontend manually:")
        print("   streamlit run timesfm_frontend.py")
        return False

if __name__ == "__main__":
    main()

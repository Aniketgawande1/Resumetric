#!/usr/bin/env python3
"""
Test script to demonstrate the email control feature
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123"

def test_analysis_without_email():
    """Test analysis without sending email"""
    print("🧪 Testing analysis WITHOUT email...")
    
    # Login first
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare test data
    files = {"resume": ("test_resume.pdf", open("aniketresume.pdf", "rb"), "application/pdf")}
    data = {
        "job_description": "We are looking for a backend developer with Python, MongoDB, Docker, and AWS experience.",
        "send_email": "false"  # ✅ Email will NOT be sent
    }
    
    # Send analysis request
    response = requests.post(f"{BASE_URL}/analyze", files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Score: {result['score']}%")
        print(f"📧 Email sent: {result.get('email_sent', False)}")
        print(f"🎯 Missing skills: {len(result['missing_skills'])}")
        return result
    else:
        print(f"❌ Analysis failed: {response.text}")
        return None

def test_analysis_with_email():
    """Test analysis with email sending"""
    print("\n🧪 Testing analysis WITH email...")
    
    # Login first
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Prepare test data
    files = {"resume": ("test_resume.pdf", open("aniketresume.pdf", "rb"), "application/pdf")}
    data = {
        "job_description": "We are looking for a backend developer with Python, MongoDB, Docker, and AWS experience.",
        "send_email": "true"  # ✅ Email WILL be sent
    }
    
    # Send analysis request
    response = requests.post(f"{BASE_URL}/analyze", files=files, data=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Score: {result['score']}%")
        print(f"📧 Email sent: {result.get('email_sent', False)}")
        print(f"🎯 Missing skills: {len(result['missing_skills'])}")
        return result
    else:
        print(f"❌ Analysis failed: {response.text}")
        return None

def test_manual_email_send(analysis_result):
    """Test manually sending email with analysis results"""
    if not analysis_result:
        print("❌ No analysis result to send")
        return
    
    print("\n🧪 Testing manual email sending...")
    
    # Login first
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = login_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Send email manually
    response = requests.post(f"{BASE_URL}/send-email", json=analysis_result, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Manual email sent successfully!")
        print(f"📧 Message: {result.get('message')}")
    else:
        print(f"❌ Manual email failed: {response.text}")

if __name__ == "__main__":
    print("🚀 Email Control Test Suite")
    print("=" * 50)
    
    # Test 1: Analysis without email
    result1 = test_analysis_without_email()
    
    # Test 2: Analysis with email
    result2 = test_analysis_with_email()
    
    # Test 3: Manual email sending
    test_manual_email_send(result1)
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📋 Summary:")
    print("- Use 'send_email': 'false' in form data to skip email")
    print("- Use 'send_email': 'true' in form data to send email")
    print("- Use /api/send-email endpoint to manually send emails")

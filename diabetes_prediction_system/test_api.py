#!/usr/bin/env python3
"""
Test script to verify the API is working correctly
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("Testing Diabetes Prediction API")
print("=" * 60)

# Test 1: Check server health
print("\n1. Testing server health...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Get model info
print("\n2. Testing model info endpoint...")
try:
    response = requests.get(f"{BASE_URL}/model/info")
    print(f"   Status: {response.status_code}")
    model_info = response.json()
    print(f"   Model type: {model_info.get('model_type')}")
    print(f"   Features: {model_info.get('features')}")
    print(f"   Threshold: {model_info.get('threshold')}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Test prediction with sample data
print("\n3. Testing prediction endpoint...")
sample_data = {
    "HighBP": 0,
    "HighChol": 0,
    "CholCheck": 1,
    "BMI": 25.5,
    "PhysActivity": 1,
    "GenHlth": 2
}

print(f"   Sending data: {sample_data}")
try:
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status: {response.status_code}")
    result = response.json()
    print(f"   Response: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 60)
print("Test completed!")
print("=" * 60)

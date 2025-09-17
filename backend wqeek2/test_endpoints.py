#!/usr/bin/env python3
"""
Endpoint Testing Script for Mechanic Shop API
This script tests all available endpoints in the Flask application.
"""

import requests
import json
from datetime import date

# Base URL for the API
BASE_URL = "http://localhost:5001"

def print_response(method, url, response, payload=None):
    """Helper function to print response details"""
    print(f"\n{'='*50}")
    print(f"{method} {url}")
    if payload:
        print(f"Payload: {json.dumps(payload, indent=2)}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2) if response.headers.get('content-type') == 'application/json' else response.text}")

def test_customer_endpoints():
    """Test all customer endpoints"""
    print("\n" + "="*60)
    print("TESTING CUSTOMER ENDPOINTS")
    print("="*60)
    
    # Test data for customers
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "555-1234"
    }
    
    updated_customer_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "555-5678"
    }
    
    # 1. Create a customer (POST /customers)
    response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    print_response("POST", "/customers", response, customer_data)
    
    if response.status_code == 201:
        customer_id = response.json().get('id')
        
        # 2. Get all customers (GET /customers/)
        response = requests.get(f"{BASE_URL}/customers/")
        print_response("GET", "/customers/", response)
        
        # 3. Get specific customer (GET /customers/<id>)
        response = requests.get(f"{BASE_URL}/customers/{customer_id}")
        print_response("GET", f"/customers/{customer_id}", response)
        
        # 4. Update customer (PUT /customers/<id>)
        response = requests.put(f"{BASE_URL}/customers/{customer_id}", json=updated_customer_data)
        print_response("PUT", f"/customers/{customer_id}", response, updated_customer_data)
        
        # 5. Delete customer (DELETE /customers/<id>)
        response = requests.delete(f"{BASE_URL}/customers/{customer_id}")
        print_response("DELETE", f"/customers/{customer_id}", response)
    
    # Test error cases
    # Try to get non-existent customer
    response = requests.get(f"{BASE_URL}/customers/999")
    print_response("GET", "/customers/999 (non-existent)", response)
    
    # Try to create customer with invalid data
    invalid_data = {"name": "Test"}  # Missing required fields
    response = requests.post(f"{BASE_URL}/customers", json=invalid_data)
    print_response("POST", "/customers (invalid data)", response, invalid_data)

def test_mechanic_endpoints():
    """Test all mechanic endpoints"""
    print("\n" + "="*60)
    print("TESTING MECHANIC ENDPOINTS")
    print("="*60)
    
    # Test data for mechanics
    mechanic_data = {
        "name": "Mike Johnson",
        "email": "mike.johnson@mechanic.com",
        "salary": 75000.0,
        "password": "secure_password123"
    }
    
    updated_mechanic_data = {
        "name": "Michael Johnson",
        "email": "michael.johnson@mechanic.com",
        "salary": 80000.0,
        "password": "new_secure_password123"
    }
    
    # 1. Create a mechanic (POST /mechanics/)
    response = requests.post(f"{BASE_URL}/mechanics/", json=mechanic_data)
    print_response("POST", "/mechanics/", response, mechanic_data)
    
    if response.status_code == 201:
        mechanic_id = response.json().get('id')
        
        # 2. Get all mechanics (GET /mechanics/)
        response = requests.get(f"{BASE_URL}/mechanics/")
        print_response("GET", "/mechanics/", response)
        
        # 3. Update mechanic (PUT /mechanics/<id>)
        response = requests.put(f"{BASE_URL}/mechanics/{mechanic_id}", json=updated_mechanic_data)
        print_response("PUT", f"/mechanics/{mechanic_id}", response, updated_mechanic_data)
        
        # 4. Delete mechanic (DELETE /mechanics/<id>)
        response = requests.delete(f"{BASE_URL}/mechanics/{mechanic_id}")
        print_response("DELETE", f"/mechanics/{mechanic_id}", response)
    
    # Test error cases
    # Try to update non-existent mechanic
    response = requests.put(f"{BASE_URL}/mechanics/999", json=updated_mechanic_data)
    print_response("PUT", "/mechanics/999 (non-existent)", response, updated_mechanic_data)

def test_ticket_endpoints():
    """Test all ticket endpoints"""
    print("\n" + "="*60)
    print("TESTING TICKET ENDPOINTS")
    print("="*60)
    
    # First, create a customer for the ticket
    customer_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "555-9999"
    }
    
    customer_response = requests.post(f"{BASE_URL}/customers", json=customer_data)
    print_response("POST", "/customers (for ticket test)", customer_response, customer_data)
    
    if customer_response.status_code != 201:
        print("Failed to create customer for ticket test")
        return
    
    customer_id = customer_response.json().get('id')
    
    # Create a mechanic for ticket assignment
    mechanic_data = {
        "name": "Bob Mechanic",
        "email": "bob.mechanic@shop.com",
        "salary": 70000.0,
        "password": "mechanic_pass123"
    }
    
    mechanic_response = requests.post(f"{BASE_URL}/mechanics/", json=mechanic_data)
    print_response("POST", "/mechanics/ (for ticket test)", mechanic_response, mechanic_data)
    
    if mechanic_response.status_code != 201:
        print("Failed to create mechanic for ticket test")
        return
    
    mechanic_id = mechanic_response.json().get('id')
    
    # Test data for tickets
    ticket_data = {
        "customer_id": customer_id,
        "service_desc": "Oil change and tire rotation"
    }
    
    # 1. Create a ticket (POST /tickets/)
    response = requests.post(f"{BASE_URL}/tickets/", json=ticket_data)
    print_response("POST", "/tickets/", response, ticket_data)
    
    if response.status_code == 201:
        ticket_id = response.json().get('id')
        
        # 2. Get all tickets (GET /tickets/)
        response = requests.get(f"{BASE_URL}/tickets/")
        print_response("GET", "/tickets/", response)
        
        # 3. Add mechanic to ticket (PUT /tickets/<id>/add-mechanic/<mechanic_id>)
        response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/add-mechanic/{mechanic_id}")
        print_response("PUT", f"/tickets/{ticket_id}/add-mechanic/{mechanic_id}", response)
        
        # 4. Remove mechanic from ticket (PUT /tickets/<id>/remove-mechanic/<mechanic_id>)
        response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/remove-mechanic/{mechanic_id}")
        print_response("PUT", f"/tickets/{ticket_id}/remove-mechanic/{mechanic_id}", response)
    
    # Test error cases
    # Try to create ticket with invalid customer_id
    invalid_ticket_data = {
        "customer_id": 999,
        "service_desc": "Invalid customer test"
    }
    response = requests.post(f"{BASE_URL}/tickets/", json=invalid_ticket_data)
    print_response("POST", "/tickets/ (invalid customer)", response, invalid_ticket_data)

def test_server_status():
    """Test if the server is running"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Server is running at {BASE_URL}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Server is not running at {BASE_URL}")
        print(f"Error: {e}")
        print("Please make sure your Flask app is running with: python app.py")
        return False

def main():
    """Run all endpoint tests"""
    print("="*60)
    print("MECHANIC SHOP API ENDPOINT TESTING")
    print("="*60)
    
    # Check if server is running
    if not test_server_status():
        return
    
    try:
        # Test all endpoints
        test_customer_endpoints()
        test_mechanic_endpoints()
        test_ticket_endpoints()
        
        print("\n" + "="*60)
        print("TESTING COMPLETED")
        print("="*60)
        
    except requests.exceptions.RequestException as e:
        print(f"Error during testing: {e}")
        print("Make sure your Flask application is running on http://localhost:5001")

if __name__ == "__main__":
    main()

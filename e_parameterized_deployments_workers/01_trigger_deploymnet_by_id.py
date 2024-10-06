import requests

# Local Prefect API URL
url = "http://localhost:4200/api/deployments/{deployment_id}/create_flow_run"

# Replace with your actual deployment ID after registration
deployment_id = "5a261f52-bc2d-45f3-9484-7d728fd9375f"


# Parameters to pass to the flow
payload = {
    "parameters": {
        "user_id": 101  # Example user ID
    }
}

# Make the API request
response = requests.post(f"http://localhost:4200/api/deployments/{deployment_id}/create_flow_run", json=payload)

# Check the response
if response.status_code == 200:
    print("Flow run triggered successfully:", response.json())
else:
    print("Error triggering flow run:", response.status_code, response.text)

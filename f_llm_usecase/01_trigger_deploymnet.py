import requests

# Function to get the deployment ID by name
def get_deployment_id_by_name(flow_name, deployment_name):
    # Local Prefect API URL to get the deployment by flow and deployment name
    url = f"http://localhost:4200/api/deployments/name/{flow_name}/{deployment_name}"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        deployment = response.json()
        return deployment['id']  # Retrieve the deployment ID from the response
    else:
        raise Exception(f"Error fetching deployment: {response.status_code} - {response.text}")

# Flow and Deployment names
flow_name = "llm-question-flow"
deployment_name = "llm-question-deployment"

try:
    # Fetch the deployment ID dynamically
    deployment_id = get_deployment_id_by_name(flow_name, deployment_name)
    print(f"Deployment ID for '{deployment_name}': {deployment_id}")

    # Parameters to pass to the flow
    payload = {
        "parameters": {
            "question": "Where was the 2020 world series played?"  # Example question
        }
    }

    # Trigger the flow run using the deployment ID
    url = f"http://localhost:4200/api/deployments/{deployment_id}/create_flow_run"
    response = requests.post(url, json=payload)

    # Check the response
    if response.status_code == 200:
        print("Flow run triggered successfully:", response.json())
    else:
        print("Error triggering flow run:", response.status_code, response.text)

except Exception as e:
    print(f"An error occurred: {str(e)}")

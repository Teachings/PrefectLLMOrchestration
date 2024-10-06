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

# Example usage
flow_name = "user-account-flow"
deployment_name = "user-account-deployment"

try:
    # Fetch the deployment ID dynamically
    deployment_id = get_deployment_id_by_name(flow_name, deployment_name)
    print(f"Deployment ID for '{deployment_name}': {deployment_id}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

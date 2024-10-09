import requests
import time
import requests

# Base URL for Prefect API
BASE_URL = "http://localhost:4200/api"

# Function to trigger a flow run
def trigger_flow_and_get_run_id(flow_name, deployment_name, question):
    # Fetch the deployment ID dynamically
    deployment_id = get_deployment_id_by_name(flow_name, deployment_name)
    print(f"Deployment ID for '{deployment_name}': {deployment_id}")

    # Parameters to pass to the flow
    payload = {
        "parameters": {
            "question": question  # Example question
        }
    }

    # Trigger the flow run using the deployment ID
    url = f"{BASE_URL}/deployments/{deployment_id}/create_flow_run"
    response = requests.post(url, json=payload)

    # Check the response
    if response.status_code in [200, 201]:  # Accept both 200 and 201 status codes
        flow_run = response.json()
        flow_run_id = flow_run['id']
        print(f"Flow run triggered successfully, ID: {flow_run_id}")
        return flow_run_id
    else:
        raise Exception(f"Error triggering flow run: {response.status_code} - {response.text}")

# Function to check the flow run status
def check_flow_run_status(flow_run_id):
    url = f"{BASE_URL}/flow_runs/{flow_run_id}"
    response = requests.get(url)

    if response.status_code == 200:
        flow_run = response.json()
        return flow_run['state']
    else:
        raise Exception(f"Error checking flow run status: {response.status_code} - {response.text}")

# Poll the flow run status until it completes
def wait_for_flow_completion(flow_run_id, check_interval=5):
    while True:
        state = check_flow_run_status(flow_run_id)
        print(f"Current flow state: {state['type']}")

        # Check if the flow is in a final state (either "COMPLETED", "FAILED", or "CANCELLED")
        if state['type'] in ["COMPLETED", "FAILED", "CANCELLED"]:
            print(f"Flow is in terminal state: {state['type']}")
            break

        # Wait for the specified interval before checking again
        time.sleep(check_interval)

    return state['type']

def get_flow_result(flow_run_id):
    url = f"{BASE_URL}/flow_runs/{flow_run_id}"
    response = requests.get(url)

    if response.status_code == 200:
        flow_run_data = response.json()

        # Print flow run state
        print(f"Flow run state: {flow_run_data['state']['type']}")

        # Get the storage key where the result is stored
        storage_key = flow_run_data['state']['data']['storage_key']
        print(f"Storage key location: {storage_key}")
    else:
        raise Exception(f"Error fetching flow run data: {response.status_code}")


# Function to get the deployment ID by name
def get_deployment_id_by_name(flow_name, deployment_name):
    # Prefect API URL to get the deployment by flow and deployment name
    url = f"{BASE_URL}/deployments/name/{flow_name}/{deployment_name}"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        deployment = response.json()
        return deployment['id']  # Retrieve the deployment ID from the response
    else:
        raise Exception(f"Error fetching deployment: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Trigger the flow with a question
    flow_name = "llm-question-flow"
    deployment_name = "llm-flow"
    question = "Who won the world series in 2020?"

    # Step 1: Trigger the flow and get the flow run ID
    flow_run_id = trigger_flow_and_get_run_id(flow_name, deployment_name, question)

    # Step 2: Wait for the flow to complete
    final_state = wait_for_flow_completion(flow_run_id, check_interval=1)

    # Step 3: Once the flow is completed, get the result
    if final_state == "COMPLETED":
        result = get_flow_result(flow_run_id)
        # print(f"LLM answered: {result}")
    else:
        print(f"Flow failed or did not complete. Final state: {final_state}")

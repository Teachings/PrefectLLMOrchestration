# Steps to Create and Execute Deployments


## Step 1: Set up Prefect Server and Worker on Remote Basement Server

1. **Install Prefect** on your basement server `ai.mtcl.lan`:

    ```bash
        pip install prefect
    ```

## Step 2: Start up Prefect Server and Worker on Basement Server

1. **Start Prefect Server** on `ai.mtcl.lan`:

   ```bash
   prefect server start
   ```

2. **Start Prefect Worker** on `ai.mtcl.lan`:

   ```bash
   prefect worker start
   ```

   This will allow your flows to be executed on this machine.

## Step 3: Create the Deployment

1. **Navigate to your project directory** on the basement server and create the deployment:

   ```bash
   prefect deploy
   ```

2. **Configure the `prefect.yaml` file**:

   In your project directory, you'll see a generated `prefect.yaml` file. Update it to include parameters and specify the entry point to your flow:

   ```yaml
   deployments:
     - name: user-account-deployment
       entrypoint: user_account_balance.py:user_account_flow
       parameters:
         user_id: 101  # Default value, but this can be overridden
       work_pool:
         name: default-agent-pool
   ```

3. **Deploy the Flow**:

   Once the `prefect.yaml` file is set, run the deployment command again to register the deployment:

   ```bash
   prefect deploy
   ```

## Step 4: Invoke Deployment Programmatically from Your Office Computer

Now that the flow is deployed on your basement server, you can trigger it programmatically from your office computer:

1. **Install Prefect** on your office machine:

   ```bash
   pip install prefect
   ```

2. **Execcute the Trigger Deployment Script to trigger the deployment**:

   ```bash
    python trigger_deployment.py
   ```

   This script will trigger the deployed flow on the basement server and pass the `user_id` parameter to the flow.

## Summary

- **Basement Server** (`ai.mtcl.lan` / `192.168.1.10`) runs the Prefect server and worker, which orchestrates and executes the flow.
- **Deployment** is created on the basement server and can be triggered from the office machine using Prefect's Python SDK.
- **Calling from Office Computer** is done via `run_deployment()` to trigger the deployment and pass parameters dynamically.

import time
import random
from prefect import flow, task
from prefect.exceptions import FailedRun

# Task that randomly fails, simulating an unreliable operation
@task(retries=3, retry_delay_seconds=5)
def fetch_user_info(user_id: int):
    # Simulate a random failure
    if random.choice([True, False]):
        print(f"Fetching user info for {user_id} failed! Retrying...")
        raise FailedRun(f"Failed to fetch user info for user ID: {user_id}")
    
    time.sleep(2)  # Simulate fetching user data
    return {"user_id": user_id, "name": "John Doe"}

@task
def check_account_balance(user_info: dict):
    time.sleep(3)  # Simulate checking account balance
    return f"{user_info['name']}, your account balance is: $1,234.56"

@task
def send_notification(balance_info: str):
    time.sleep(1)  # Simulate sending email notification
    return f"Notification sent: {balance_info}"

# Flow to demonstrate retries and dependent task execution
@flow
def user_account_flow(user_id: int):
    # Step 1: Fetch user info with retries if it fails
    user_info = fetch_user_info.submit(user_id)

    # Step 2: Check account balance (depends on user_info)
    balance_task = check_account_balance.submit(user_info.result())
    
    # Step 3: Send notification (depends on balance check being complete)
    notification_task = send_notification.submit(balance_task.result())

    # Collect results
    notification_result = notification_task.result()

    return notification_result

if __name__ == "__main__":
    # Run the flow
    result = user_account_flow(101)
    print(result)

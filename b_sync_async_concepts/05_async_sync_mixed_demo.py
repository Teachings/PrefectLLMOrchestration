import time
from prefect import flow, task

# Simulate tasks
@task
def fetch_user_info(user_id: int):
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

@task
def update_user_preferences(user_info: dict):
    time.sleep(2)  # Simulate updating preferences
    return f"Preferences updated for {user_info['name']}"

# Flow to demonstrate both dependent and parallel execution
@flow
def user_account_flow(user_id: int):
    # Step 1: Fetch user info (this must happen first)
    user_info = fetch_user_info.submit(user_id)

    # Step 2: Check account balance (depends on user_info)
    balance_task = check_account_balance.submit(user_info.result())
    
    # Step 3: Send notification (depends on balance check being complete)
    notification_task = send_notification.submit(balance_task.result())

    # Step 4: In parallel, update user preferences (can run independently after fetching user info)
    preferences_task = update_user_preferences.submit(user_info.result())

    # Collect results
    notification_result = notification_task.result()  # Notification result
    preferences_result = preferences_task.result()  # Preferences update result

    # Return final result combining both outcomes
    return f"{notification_result}\n{preferences_result}"

if __name__ == "__main__":
    # Run the flow
    result = user_account_flow(101)
    print(result)

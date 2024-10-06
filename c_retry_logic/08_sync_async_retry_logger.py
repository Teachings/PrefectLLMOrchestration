import time
import random
from prefect import flow, task, get_run_logger
from prefect.exceptions import FailedRun

# Utility function to simulate failure with a configurable failure rate
def simulate_failure(failure_rate=0.3):
    if random.random() < failure_rate:
        raise FailedRun("Simulated task failure.")

# Task to fetch user info with logging and potential failure
@task(retries=3, retry_delay_seconds=5)
def fetch_user_info(user_id: int):
    logger = get_run_logger()
    logger.info(f"Fetching user info for user ID: {user_id}...")
    
    # Simulate failure (30% chance)
    simulate_failure(failure_rate=0.3)
    
    time.sleep(2)  # Simulate fetching user data
    user_info = {"user_id": user_id, "name": "John Doe"}
    logger.info(f"Successfully fetched user info: {user_info}")
    return user_info

# Task to check account balance
@task
def check_account_balance(user_info: dict):
    logger = get_run_logger()
    logger.info(f"Checking account balance for {user_info['name']}...")
    
    # Simulate failure (20% chance)
    simulate_failure(failure_rate=0.2)
    
    time.sleep(3)  # Simulate checking account balance
    balance_info = f"{user_info['name']}, your account balance is: $1,234.56"
    logger.info(f"Account balance retrieved: {balance_info}")
    return balance_info

# Task to send notification
@task
def send_notification(balance_info: str):
    logger = get_run_logger()
    logger.info(f"Sending notification for: {balance_info}")
    
    # Simulate failure (10% chance)
    simulate_failure(failure_rate=0.1)
    
    time.sleep(1)  # Simulate sending email notification
    logger.info("Notification sent successfully.")
    return f"Notification sent: {balance_info}"

# Task to update user preferences
@task
def update_user_preferences(user_info: dict):
    logger = get_run_logger()
    logger.info(f"Updating preferences for {user_info['name']}...")
    
    # Simulate failure (20% chance)
    simulate_failure(failure_rate=0.2)
    
    time.sleep(2)  # Simulate updating preferences
    logger.info(f"Preferences updated for {user_info['name']}")
    return f"Preferences updated for {user_info['name']}"

# Flow to demonstrate both dependent and parallel execution with logging
@flow
def user_account_flow(user_id: int):
    logger = get_run_logger()
    logger.info(f"Starting user account flow for user ID: {user_id}")
    
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

    logger.info("Flow completed successfully.")
    return f"{notification_result}\n{preferences_result}"

if __name__ == "__main__":
    # Run the flow
    result = user_account_flow(101)
    print(result)

#user_account_balance.py
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
    
    simulate_failure(failure_rate=0.3)
    
    time.sleep(2)  # Simulate fetching user data
    user_info = {"user_id": user_id, "name": "John Doe"}
    logger.info(f"Successfully fetched user info: {user_info}")
    return user_info

# Task to check account balance
@task(retries=3, retry_delay_seconds=5)
def check_account_balance(user_info: dict):
    logger = get_run_logger()
    logger.info(f"Checking account balance for {user_info['name']}...")
    
    simulate_failure(failure_rate=0.2)
    
    time.sleep(3)  # Simulate checking account balance
    balance_info = f"{user_info['name']}, your account balance is: $1,234.56"
    logger.info(f"Account balance retrieved: {balance_info}")
    return balance_info

# Task to send notification
@task(retries=3, retry_delay_seconds=5)
def send_notification(balance_info: str):
    logger = get_run_logger()
    logger.info(f"Sending notification for: {balance_info}")
    
    simulate_failure(failure_rate=0.1)
    
    time.sleep(1)  # Simulate sending email notification
    logger.info("Notification sent successfully.")
    return f"Notification sent: {balance_info}"

# Task to update user preferences
@task(retries=3, retry_delay_seconds=5)
def update_user_preferences(user_info: dict):
    logger = get_run_logger()
    logger.info(f"Updating preferences for {user_info['name']}...")
    
    simulate_failure(failure_rate=0.2)
    
    time.sleep(2)  # Simulate updating preferences
    logger.info(f"Preferences updated for {user_info['name']}")
    return f"Preferences updated for {user_info['name']}"

# Flow to demonstrate both dependent and parallel execution with logging
@flow
def user_account_flow(user_id: int):
    logger = get_run_logger()
    logger.info(f"Starting user account flow for user ID: {user_id}")
    
    # Fetch user info
    user_info = fetch_user_info.submit(user_id)

    # Check account balance
    balance_task = check_account_balance.submit(user_info.result())
    
    # Send notification
    notification_task = send_notification.submit(balance_task.result())

    # Update user preferences in parallel
    preferences_task = update_user_preferences.submit(user_info.result())

    # Collect results
    notification_result = notification_task.result()
    preferences_result = preferences_task.result()

    logger.info("Flow completed successfully.")
    return f"{notification_result}\n{preferences_result}"

if __name__ == "__main__":
    # You can test the flow locally by running it manually
    result = user_account_flow(101)
    print(result)

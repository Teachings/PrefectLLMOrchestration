import time
from prefect import flow, task

# Tasks for demo
@task
def greet_user(name: str):
    time.sleep(2)  # Simulating a delay
    return f"Hello, {name}!\n"
    
@task
def provide_status_update(name: str):
    time.sleep(3)  # Simulating a delay
    return f"{name}, your current status is: Active\n"
    
@task
def fetch_account_balance(name: str):
    time.sleep(5)  # Simulating a longer delay
    return f"{name}, your account balance is: $1,234.56\n"

# Synchronous Flow
@flow
def user_notification_sync_flow(user_name: str):
    # Tasks run one after the other (synchronous execution)
    greeting_task = greet_user(user_name)
    status_task = provide_status_update(user_name)
    balance_task = fetch_account_balance(user_name)

    # Combine results sequentially
    final_message = greeting_task + status_task + balance_task
    return final_message

if __name__ == "__main__":
    # Synchronous execution demo
    print("Synchronous Flow (Tasks run sequentially):")
    result_sync = user_notification_sync_flow("John")
    print(result_sync)

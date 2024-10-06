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


# Asynchronous Flow
@flow
def user_notification_async_flow(user_name: str):
    # Trigger the tasks to run in parallel (asynchronous execution)
    greeting_task = greet_user.submit(user_name)  # .submit() allows tasks to run concurrently
    status_task = provide_status_update.submit(user_name)
    balance_task = fetch_account_balance.submit(user_name)

    # Collect the results once all tasks are complete
    final_message = greeting_task.result() + status_task.result() + balance_task.result()
    return final_message

if __name__ == "__main__":
    # Asynchronous execution demo
    print("Asynchronous Flow (Tasks run in parallel):")
    result_async = user_notification_async_flow("John")
    print(result_async)

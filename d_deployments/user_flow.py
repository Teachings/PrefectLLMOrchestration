from prefect import flow, task

@task
def fetch_user_info(user_id: int):
    # Simulate fetching user info
    return {"user_id": user_id, "name": "John Doe"}

@flow
def user_account_flow(user_id: int = 101):
    user_info = fetch_user_info(user_id)
    return f"Fetched info: {user_info}"

if __name__ == "__main__":
    user_account_flow()
    
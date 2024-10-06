from prefect import flow, task

@task
def say_message(msg: str):
    return msg + "\n"
    
@flow
def say_message_flow(msg: str):
    # Create tasks and concatenate their results
    task_message = say_message(msg)
    return task_message
    
if __name__ == "__main__":
    result = say_message_flow("Hello")
    print(result)

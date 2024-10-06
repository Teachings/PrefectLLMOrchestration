from prefect import flow

@flow
def say_message_flow():
    print("Hello")
    
if __name__ == "__main__":
    say_message_flow()

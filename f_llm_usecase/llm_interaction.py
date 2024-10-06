import time
from prefect import flow, task, get_run_logger
from openai import OpenAI

# Initialize OpenAI client with Ollama
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',  # Required but unused for Ollama
)

# Task to send a question to the LLM model and get a response
@task(retries=3, retry_delay_seconds=5)
def ask_llm_question(question: str):
    logger = get_run_logger()
    logger.info(f"Asking LLM the question: {question}")
    
    response = client.chat.completions.create(
      model="llama3.2",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
      ]
    )
    
    answer = response.choices[0].message.content
    logger.info(f"LLM response: {answer}")
    return answer

# Flow to handle the LLM question-answering process
@flow
def llm_question_flow(question: str):
    logger = get_run_logger()
    logger.info(f"Starting LLM question flow for question: {question}")
    
    # Ask the LLM a question
    answer = ask_llm_question.submit(question)
    
    # Collect the result
    result = answer.result()
    
    logger.info(f"Flow completed with LLM answer: {result}")
    return result

if __name__ == "__main__":
    # Test the flow locally by running it manually
    # result = llm_question_flow("Tell me a Joke")
    # print(result)
    llm_question_flow("Tell me a Joke")
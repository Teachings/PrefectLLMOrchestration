from prefect import flow, task, get_run_logger
from hooks import on_flow_completion, on_flow_failure
from prefect.serializers import JSONSerializer
from openai import OpenAI

# Initialize OpenAI client with Ollama
client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',  # Required but unused for Ollama
)

# Task to send a question to the LLM model and get a response
@task(retries=3, retry_delay_seconds=5, persist_result=True, result_serializer=JSONSerializer())
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

@flow(persist_result=True, result_serializer=JSONSerializer(), on_completion=[on_flow_completion], on_failure=[on_flow_failure])
async def llm_question_flow(question: str):
    answer = ask_llm_question(question)
    return answer

if __name__ == "__main__":
    import asyncio
    asyncio.run(llm_question_flow("Tell me a joke"))

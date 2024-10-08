from models import FlowResult, SessionLocal
import datetime
from prefect import get_run_logger

# Helper function to extract the result
def extract_result(result):
    # If the result has metadata, extract only the actual result
    if hasattr(result, 'result'):
        return result.result  
    return result  

# Async function to store result in the database
async def store_result(flow_run_id, flow_name, result, status):
    logger = get_run_logger()
    with SessionLocal() as db:
        try:
            # Extract the actual result if it's wrapped in a ResultRecord
            final_result = extract_result(result)
            
            flow_result = FlowResult(
                flow_run_id=flow_run_id,
                flow_name=flow_name,
                result={"answer": str(final_result)},  # Ensure it's serializable
                status=status,
                completed_at=datetime.datetime.utcnow()
            )
            db.add(flow_result)
            db.commit()
            logger.info(f"Stored flow result for {flow_name} with status {status}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to store result: {e}")


# Hook for flow completion
async def on_flow_completion(flow, flow_run, state):
    result = state.result()
    await store_result(flow_run.id, flow.name, result, "success")

# Hook for flow failure
async def on_flow_failure(flow, flow_run, state):
    await store_result(flow_run.id, flow.name, str(state.result), "failed")

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger("sql_agent")

def log_query(query, user_question, result=None, error=None):
    if error:
        logger.error(f"User: {user_question} | Query: {query} | Error: {error}")
    else:
        logger.info(f"User: {user_question} | Query: {query} | Result: {result}")

from langchain.llms import OpenAI
from langchain.agents import create_pandas_dataframe_agent
import os

def get_chat_response(query, df):
    llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
    agent = create_pandas_dataframe_agent(llm, df, verbose=False)
    return agent.run(query)

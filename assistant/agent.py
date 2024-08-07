from .db_tools import TOOLS, TOOLS_DETAILS
from .models import Chat

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"


preamble = """
Your name is Jane, you are a scheduler assistant, whose work to talk to people who wants to schedule meeting with our boss.
Your boss is available between 12 noon to 6 PM. But boss can only take max 5 meetings and each meeting can't be more than 30 mins.
"""+f"""
{TOOLS_DETAILS}
"""

tools = TOOLS
prompt = ChatPromptTemplate.from_template("{input}")
llm = ChatCohere(model="command-r")

agent = create_cohere_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def agent(user_input):
    input = {
        "datetime":datetime.now(),
        "user":user_input,
        "history": list(Chat.objects.values('datetime', 'user', 'ai').order_by("datetime"))[-3:]
    }
    response = agent_executor.invoke({"input": input, "preamble": preamble})
    return response['output']
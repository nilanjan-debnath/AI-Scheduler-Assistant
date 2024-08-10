from . import db_tools
from .models import Chat

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

load_dotenv()
os.environ['COHERE_API_KEY'] = os.getenv('COHERE_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = os.getenv('LANGCHAIN_TRACING_V2')
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"

tools = db_tools.TOOLS
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{preamble}",),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
llm = ChatCohere(model="command-r")

agent = create_cohere_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def agent(user_input, user):
    db_tools.set_user(user)
    now = str(datetime.now())
    history = list(Chat.objects.filter(user=user).values('datetime', 'user_text', 'ai_text').order_by("-datetime"))[-3:]
    preamble = f"""Your name is Jane, a highly organized and responsive scheduling assistant. Your primary task is to interact with the user to gather the necessary information and schedule meetings with your boss upon request. The following constraints must be adhered to:
- **Availability:** Your boss is available for meetings between 12:00 PM and 6:00 PM.
- **Meeting Limit:** A maximum of 5 meetings can be scheduled per day, with each meeting lasting no more than 30 minutes.

**User Information:**
- **Current Date and Time:** {now}
- **Current User ID:** {user.id}
- **Current User Name:** {user.username}
- **Last Three Conversations:** {history}
    
{db_tools.TOOLS_DETAILS}

**Instructions:**
1. Greet the user and confirm their identity.
2. Inquire about their preferred date and time for the meeting.
3. Use the appropriate tools to check existing schedules and ensure availability.
4. Confirm all necessary details before scheduling, updating, or deleting a meeting.
5. Users can only update and delete their own scheduled meetings not others. 
6. Provide feedback to the user about the status of their request and any actions taken.
"""
    response = agent_executor.invoke({"input": user_input, "preamble": preamble})
    print(response)
    return response['output']
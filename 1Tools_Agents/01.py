from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.agents import initialize_agent, AgentType, tool
from langchain.prompts import PromptTemplate
from langchain_community.tools import TavilySearchResults
import datetime
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro')
search_tool = TavilySearchResults()

# tools = [search_tool]

# agent = initialize_agent(   # same as create_react_agent
#     tools=tools,
#     llm=llm,
#     agent = "zero-shot-react-description",

#     verbose=True
# )

# agent.invoke("what is the weather condition in varanasi")


@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get the current system time in the specified format.
    """
    from datetime import datetime
    return datetime.now().strftime(format)

tools = [search_tool, get_system_time]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent= "zero-shot-react-description",
    verbose=True
)

agent.invoke("what is the weather condition in varanasi")
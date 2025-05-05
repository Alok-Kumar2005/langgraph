from langgraph.graph import MessageGraph, END, StateGraph , START, MessagesState
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import tools_condition , ToolNode
from IPython.display import display, Image
from typing import Annotated, TypedDict
import operator
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-pro")


def multiply(a: int, b: int) -> int:
    """Multiply a and b.
    Args:
        a: First number
        b: Second number
        """
    return a * b


def add(a: int, b: int) -> int:
    """Add a and b.
    Args:
        a: First number
        b: Second number
        """
    return a + b


search = DuckDuckGoSearchRun()

# print(search.invoke("how is the current president of the USA"))

tools = [add , multiply, search]

llm_with_tools = llm.bind_tools(tools)


sys_msg = SystemMessage(content = "You are a helpful assistant that can perform basic math operations and search the web.")

def reasoner(state: MessagesState) -> str:
    """Reasoner function that takes a state and returns a string."""
    return {
        "messages": [llm_with_tools.invoke([sys_msg]+state["messages"])]
    }


builder = StateGraph(MessagesState)
builder.add_node("reasoner", reasoner)
builder.add_node("tools" , ToolNode(tools))
## Add edges
builder.add_edge(START, "reasoner")
builder.add_conditional_edges(
    "reasoner",
    tools_condition,
)

builder.add_edge("tools", "reasoner")
react_graph = builder.compile()



messages = [HumanMessage(content="what is 2 times of Rahul Gandhi age?")]
messages = react_graph.invoke({"messages": messages})["messages"]
print(messages)


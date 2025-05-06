from typing import TypedDict, List, Any, Callable, Dict, Optional , Annotated
from langgraph.graph import add_messages , StateGraph, END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)

memory = SqliteSaver(sqlite_conn)


class BasicChatbotState(TypedDict):
    messages: Annotated[list , add_messages]


def chatbot(state: BasicChatbotState):
    """Chatbot function that takes a state and returns a string."""
    return {
        "messages": [llm.invoke(state["messages"])]
    }


graph = StateGraph(BasicChatbotState)
graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

app = graph.compile(checkpointer=memory)


config = {"configurable": {
    "thread_id": 1
}}

while True:
    user_input = input("enter your message: ")
    if (user_input.lower() in ["exit", "quit"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config = config)
        # print(result['messages'][-2].content)
        print(result['messages'][-1].content)


from typing import TypedDict, List, Any, Callable, Dict, Optional , Annotated
from langgraph.graph import add_messages , StateGraph, END, MessagesState , ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

class BasicChatbotState(TypedDict):
    messages: Annotated[list , add_messages]

seach_tool = TavilySearchResults(search_depth="basic")
tools = [seach_tool]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: BasicChatbotState):
    """Chatbot function that takes a state and returns a string."""
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }


def tools_router(state: BasicChatbotState):
    last_message = state["messages"][-1]
    if(hasattr(last_message, "tool_calls") and len (last_message.tool_calls)>0):
        return "tool_node"
    else:
        return END
    

tool_node = ToolNode(tools = tools)
graph = StateGraph(BasicChatbotState)
graph.add_node("chatbot", chatbot)
graph.add_node("tools", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tools", "chatbot")
graph.add_edge("chatbot", END)


while True:
    user_input = input("enter your message: ")
    if (user_input.lower() in ["exit", "quit"]):
        break
    else:
        result = graph.invoke({
            "messages": [HumanMessage(content=user_input)]
        })
        print(result['messages'][-1].content)
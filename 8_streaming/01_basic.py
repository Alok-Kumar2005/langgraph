from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from typing import TypedDict, Annotated
from langgraph.graph import add_messages , StateGraph , END
from langgraph.prebuilt import ToolNode


load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]


llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-pro')
llm_with_tools = llm.bind_tools(tools=tools)


def model(state: AgentState):
    return {
        "messages": [llm_with_tools.invoke(state['messages'])],
    }

def tools_router(state: AgentState):
    last_message = state['messages'][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0 ):
        return "tool_node"
    else:
        return END
    

tool_node = ToolNode(tools = tools)
graph = StateGraph(AgentState)
graph.add_node("model", model)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("model")

graph.add_conditional_edges("model", tools_router)
graph.add_edge("tool_node", "model")

app = graph.compile()


# input = {
#     "messages":["What is the current weather in Varanasi"]
# }
# events = app.stream(input = input , stream_mode = "values")

# for event in events:
#     print(event['messages'])


# input = {
#     "messages":["What is the current weather in Varanasi"]
# }

# events = app.stream(input = input , stream_mode = "updates")

# for event in events:
#     print(event)




"""
STREAMING IN LANGGRAPH
In prod apps, we usually want to stream more than the state
in Particular, with LLM calls it is common to stream the tokens they are generated 
"""


##### how to get the each token 
## ( whenever a tool is call , what it read we got from here )

# input = {
#     "messages": ["Hi, how are you?"]
# }

# import asyncio

# async def process_events():
#     events = app.astream_events(input=input, version="v2")
#     async for event in events: 
#         print(event)

# # Run the async function
# asyncio.run(process_events())



input = {
    "messages": ["Hi, how are you?"]
}

import asyncio

async def process_events():
    events = app.astream_events(input=input, version="v2")
    async for event in events: 
        if event["event"] == "on_chat_model_stream":
            print(event["data"]["chunk"].content, end="")

# Run the async function
asyncio.run(process_events())
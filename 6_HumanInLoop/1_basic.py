"""
there are 3 types of human in the loop:
1. Approve or Reject: the human can approve or reject the output of the LLM. This is useful when the LLM is not sure about the answer and needs human validation.
2. Edit: the human can review and edit the output of the LLM. This is useful when the LLM is not sure about the answer and needs human validation.
3. REview: the human can review the output of the LLM. This is useful when the LLM is not sure about the answer and needs human validation.
"""

from typing import TypedDict , List , Annotated
from langchain_core.messages import SystemMessage , HumanMessage , AIMessage
from langgraph.graph import add_messages , StateGraph , END , MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    messages: Annotated[list , add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")


GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"


def generate_post(state: State) -> State:
    return {
        "messages": [llm.invoke(state["messages"])]
    }


def get_review_decision(state: State):
    post_content = state["messages"][-1].content

    print(f"Post content: {post_content}")
    print("\n")

    decision = input("Do you want to approve the post? (yes/no): ")
    if decision.lower() == "yes":
        return POST
    else:
        return COLLECT_FEEDBACK
    
def post(state: State):
    final_post = state["messages"][-1].content
    print(f"Final post: {final_post}")
    print("\n")
    print("Post has been published!")

def collect_feedback(state: State):
    feedback = input("Please provide your feedback on the post: ")
    return {
        "messages": [AIMessage(content=feedback)]
    }

graph = StateGraph(State)

graph.add_node(GENERATE_POST , generate_post)
graph.add_node(GET_REVIEW_DECISION , get_review_decision)
graph.add_node(POST , post)
graph.add_node(COLLECT_FEEDBACK , collect_feedback)

graph.set_entry_point(GENERATE_POST)
graph.add_conditional_edges(GENERATE_POST , get_review_decision)
graph.add_edge(POST , END)
graph.add_edge(COLLECT_FEEDBACK , GENERATE_POST)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content = "Write a post on Ai Agent taking over content creation")]
})

print(response)



"""
Some drawbacks of input():
1. Freezes your program completely until someone types something
2. Only workd in terminals- useless for webapps
3. if program crashes, all progress is lost
4. can only handle one user at a time
5. lives only in our terminal


so we are going to use interrupt()
"""








from typing import List , TypedDict, Annotated
from langgraph.graph import MessageGraph, END, StateGraph
import operator


class SimpleState(TypedDict):
    count :int
    sum: Annotated[int, operator.add]
    history: Annotated[List[int] , operator.concat]

def increment(state: SimpleState) -> SimpleState:
    return {
        "count": state["count"] + 1,
        "sum": state["count"] + 1,
        "history": [state["count"] + 1]
    }


def should_continue(state: SimpleState) -> str:
    if state["count"] > 5:
        return END
    return "increment"
    


graph = StateGraph(SimpleState)

graph.add_node("increment", increment)
graph.add_conditional_edges("increment", should_continue)
graph.set_entry_point("increment")

app = graph.compile()


state = {
    "count": 0,
    "sum": 0,
    "history": []
}

result = app.invoke(state)
print(result)
"""
ReAct Agent in Langchain
1. create_react_agent
- takes each tool name and description 
- format them into a standardized way the LLM can understand
- Inserts them into specific placeholders in the ReAct prompt template
- It make the LLM call + take the LLM response + parse the response

- It return AgentAction class or AgentFinish class

AgentAction class
- this is a langchain class that represents an action the agent wants to take

AgentFinish class
- this is a langchain class that represents the final answer the agent wants to return


2. AgentExecutor
- takes the agent from create_react_agent and the tools and manages the execution loop
- Receives the user question and feed it to the agent
- Identifies which tool to use based on the agent's response



ReAct Agent in Langgraph
- The 'reason' node does what create_react_agent did it thinks and decides
- if the reason node outputs an AgentAction, then "act" node executes the tool
- Results from the tool flow back to reason node from the next decision


"""
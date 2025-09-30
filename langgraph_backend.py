from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,List,Annotated


load_dotenv()
#importing in memory to save the messages in the memory 
#to add the messeages in the state
from langgraph.graph.message import add_messages,BaseMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,SystemMessage

class ChatState(TypedDict):
    messages=Annotated[List[BaseMessage],add_messages]

model=ChatOpenAI(model='gpt-4')

def chatting_function(state: ChatState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':[response]}
    
    

#graph
chatbot=StateGraph(ChatState)

#graph nodes

chatbot.add_node('chat',chatting_function)


#graph edges
chatbot.add_edge(START,'chat')
chatbot.add_edge('chat',END)

#compiling the graph with giving checkpointer as a argument for persistence
#initlializing the checkpointer
checkpointer=MemorySaver()
workflow=chatbot.compile(checkpointer=checkpointer)


#executing the workflow for a test case
#initializing a thread for a unique id
thread_id=1
CONFIG={'configurable':{'thread_id':thread_id}}

initial_state={'messages':'hi how are you doing today'}
final_state=workflow.invoke(initial_state,config=CONFIG)
print(final_state)

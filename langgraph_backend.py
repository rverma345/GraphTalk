from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,List,Annotated


load_dotenv()
#to add the messeages in the state
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    messages=Annotated[List[str],add_messages]
#importing in memory to save the messages in the memory 
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,SystemMessage
prompt=(
        [SystemMessage(content='You are a Helpful assistant that provides user with helpful and factual answers')],
        [HumanMessage(content='You are need to provide response to the user such that it follows the following rules:' \
        '1. the results should be factually correct'
        "2. Do not make up facts yourself if you dont have the information needed for the question just tell you don't know")]
    )

model=ChatOpenAI(model='gpt-4')

def chatting_function(state: ChatState):
    response=model.invoke(prompt)
    return {'messages':response}
    
    

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

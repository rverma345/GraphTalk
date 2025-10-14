from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,List
from langgraph.graph.message import BaseMessage,add_messages
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


load_dotenv()

llm=ChatOpenAI()

#defining the state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

# defining the chat node function

def chat_node(state: ChatState):
    message=state['messages']
    response=llm.invoke(message).content
    return {"messages":[response]}



conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
# checkpointer
checkpointer=SqliteSaver(conn=conn)

# graph inilialization
graph=StateGraph(ChatState)

# nodes
graph.add_node('chat_node',chat_node)


#adding edges 

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


# compiling the graph 

Chatbot=graph.compile(checkpointer=checkpointer)

CONFIG={'configurable':{'thread_id':'thread-2'}}
response=Chatbot.invoke(
    {'messages': [HumanMessage(content='what is my name')]},
    config=CONFIG
)
print(response)
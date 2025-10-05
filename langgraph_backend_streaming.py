from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict,Annotated,List
from langgraph.graph.message import BaseMessage,add_messages
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver


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

# checkpointer
checkpointer=MemorySaver()

# graph inilialization
graph=StateGraph(ChatState)

# nodes
graph.add_node('chat_node',chat_node)


#adding edges 

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)


# compiling the graph 

Chatbot=graph.compile(checkpointer=checkpointer)

for message_chunk,metadata in Chatbot.stream(
    {'messages': HumanMessage(content='what is the recepie for pasta')},
    config={'configurable':{'thread_id':'thread-1'}},
    stream_mode='messages',
):
    if message_chunk.content:
        print(message_chunk.content, end=' ',flush=True)
    

from tutorial_quickstart.tool.tools import CREATE_CALENDAR_EVENT,SEARCH_CALENDAR_EVENT,DELETE_CALENDAR_EVENT,UPDATE_CALENDAR_EVENT
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from copilotkit import CopilotKitState
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import Literal
from tutorial_quickstart.Prompt import PROMPT
import datetime
import os
load_dotenv()

class Appointment:
    
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY"))
        self.tools = [
                CREATE_CALENDAR_EVENT,
                SEARCH_CALENDAR_EVENT,
                DELETE_CALENDAR_EVENT,
                UPDATE_CALENDAR_EVENT
                ]
        self.schedule_tools = [SEARCH_CALENDAR_EVENT]
 
 

    def chat_bot(self,state: CopilotKitState):
        messages = state["messages"]
        today_datetime = datetime.datetime.now().isoformat()
        print(today_datetime)
        input_messages = [SystemMessage(content=PROMPT(today_datetime=today_datetime))]
        
        for msg in messages:
            print(msg)                    # edited new line
            if isinstance(msg, HumanMessage):
                input_messages.append(msg)
            elif hasattr(msg, 'tool_calls') and msg.tool_calls:
                input_messages.append(msg)
            elif hasattr(msg, 'tool_call_id'):
                if not isinstance(msg.content, str):
                    msg.content = str(msg.content)
                input_messages.append(msg)
            else:
                input_messages.append(msg)
                
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(input_messages)
        return {"messages": [response]}


    def tools_condition(self,state: CopilotKitState) -> Literal["find_slots",  "tool", "__end__"]:
        """
        Determine if the conversation should continue to tools or end
        """
        messages = state["messages"]
        last_message = messages[-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for call in last_message.tool_calls:
                tool_name = call.get("name")
                
                if tool_name == "SEARCH_CALENDAR_EVENT":
                    return "find_slots"
            return "tool"

        return "__end__"

    def find_slots(self,state: CopilotKitState) -> Literal["Chatbot"]:
        """
        Determine if the conversation should continue to tools or end
        """
        messages = state["messages"]
        last_message = messages[-1]

        tool_messages = []
        print("find slot called")
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            
            for call in last_message.tool_calls:
                tool_name = call.get("name")
                tool_id = call.get("id")
                args = call.get("args")

                find_free_slots_tool = next(
                        (tool for tool in self.schedule_tools if tool.name == tool_name), None)

                if tool_name == "SEARCH_CALENDAR_EVENT":

                    res = find_free_slots_tool.invoke(args)
                    tool_msg = ToolMessage(
                            name=tool_name,
                            content=f"{res}",
                            tool_call_id=tool_id  
                        )
                    tool_messages.append(tool_msg)
        return {"messages": tool_messages}


    def __call__(self):
        workflow = StateGraph(CopilotKitState)
        workflow.add_node("Chatbot", self.chat_bot)
        workflow.add_node("find_slots", self.find_slots)
        workflow.add_node("tool", ToolNode(self.tools))
        workflow.add_edge(START, "Chatbot")
        workflow.add_conditional_edges(
            "Chatbot",
            self.tools_condition,
            {
                "tool": "tool",        
                "find_slots": "find_slots", 
                "__end__": END       
            }
        )
        workflow.add_edge("tool", "Chatbot")
        workflow.add_edge("find_slots", "Chatbot")
        memory = MemorySaver()
        graph = workflow.compile(checkpointer=memory)
        
        return graph
# clss10
from agents import Agent,Runner,set_tracing_disabled,RunConfig,TResponseInputItem,handoff,RunContextWrapper,HandoffInputData
from my_agents.flight_agent import flight_agent
from my_agents.hotel_agent import hotel_agent
from my_agents.weather_agent import weather_agent
import asyncio
from my_config.config import run_config
from typing import Literal
from pydantic import BaseModel 
from agents.extensions import handoff_filters

set_tracing_disabled(True)

class User(BaseModel):
    name:str
    role:Literal["admin","super user","basic"]
    age:int
    
 #5   
async def handoff_permission(ctx:RunContextWrapper[User],agent:Agent)->bool:
    if ctx.context.age > 19 and ctx.context.role == "super user": # and sai nh hoga or kryga tu hojaega
        return True
    
    if ctx.context.role == "super user":
        return True
    
    return False 

# 6 input filter k liye
async def handoff_filter(data:HandoffInputData)->HandoffInputData:
    data = handoff_filters.remove_all_tools(data) # remove tool calling all hojaegi token save input hoga bs 
    history =  data.input_history[-2:]
    
    return HandoffInputData(
        input_history=history,
        pre_handoff_items=data.pre_handoff_items,
        new_items=data.new_items
    )
   # return data

triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are triage agent,hands off to flight,hotel or weather agent if user ask for
    otherwise you can response yourself
    """,
    #3
    handoffs=[
        #4
        handoff(
            weather_agent,
            tool_name_override="handoff_weatheragent",
            tool_description_override="handoff to weather to get the weather information",
            #is_enabled=True # false hoga nh answer dyga true mai answer dyga
            is_enabled=handoff_permission,
            input_filter=handoff_filter
            ),
            
        flight_agent,
        hotel_agent],
    handoff_description="""    
   this triage agent, hand off to flight,
   hotel or weather agent if user ask for otherwise you can response yourselfffff 
    """    
)

async def main():
    user = User(name="abc",role="admin",age=20)
    start_agent = triage_agent
    # dirct answer i will travel to lahore
    input_data :list[TResponseInputItem] = []
    #2
    while True:
        #1
        user_prompt = input("enter your query: ")
        if user_prompt == "exit":
            break
        
        input_data.append({
            "role":"user",
            "content":user_prompt
        })
        
        # result = await Runner.run(triage_agent,user_prompt,run_config=run_config)
        
        result = await Runner.run(start_agent,input=input_data,run_config=run_config,context=user)
        
        # weather query start triage sai then weather agent or isi ko run krta rhyga 
        start_agent = result.last_agent
        
        #print(result) check 
        
        print(result.final_output)
        
#7  quer change hotel or flight hand off triage agent        
weather_agent.handoffs.append(triage_agent)

flight_agent.handoffs.append(triage_agent)

hotel_agent.handoffs.append(triage_agent)
    
asyncio.run(main())

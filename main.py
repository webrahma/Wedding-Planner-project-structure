from prompts import WEDDING_PLANNER_AGENT_PROMPT, USER_PROMPT_FOR_MAIN_AGENT
from langchain.agents import create_agent
from models import llm
from agent import delegate_to_subagent1,delegate_to_subagent2
from langchain.messages import HumanMessage


import logging

logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s  | %(levelname)s  | %(message)s"
    )

if __name__ == "__main__":
    #asking user for their requiment  for their wedding 
    logging.info("asking user for their requirements ....")    
    user_requireminput=input("please enter your requirements and preferences for your wedding:\n ")

    #updating the system prompt
    updated_system_prompt = WEDDING_PLANNER_AGENT_PROMPT.format(requirements=user_requireminput)

    #creating main agent 
    logging.info("initializing main wedding planner agent ...")
    main_wedding_planner_agent=create_agent(
        model=llm,
        tools=[delegate_to_subagent1,delegate_to_subagent2],
        name="MainWeddingPlanner",
        system_prompt=updated_system_prompt
    )

    #invoke main agent 
    logging.info("invoking main wedding planner agent...")
    response_main_agent=main_wedding_planner_agent.invoke({"messages":[HumanMessage(content=USER_PROMPT_FOR_MAIN_AGENT)]}) 

    #print the response of the main agent 
    print("\nMain wedding planner Agent's response: ")
    print(response_main_agent["messages"][-1].content)



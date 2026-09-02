from crewai import Task,Agent,Process,Crew,LLM
from crewai.project import CrewBase,agent,task,crew
from Scheme import CandidateProfile
from Tools import github_profile_tool,Linked_in_Profile_Tool
from dotenv import load_dotenv
import os
import agentops

load_dotenv()
llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.5,
)

@CrewBase
class Discovery_crew:
    agents_config  = r"F:\Job_Hunter_Agent_Crew\Src\Crew\Discovery_Crew\config\Agents.yaml"
    tasks_config = r"F:\Job_Hunter_Agent_Crew\Src\Crew\Discovery_Crew\config\Tasks.yaml"

    @agent
    def Profile_Analyst_Agent(self)->Agent:
        return Agent(
            config = self.agents_config ["Profile_Analyst_Agent"],
            tools = [github_profile_tool,Linked_in_Profile_Tool],
            llm = llm,
            verbose = True
        )
    
    @task
    def Profile_Analyst_Task(self)->Task:
        return Task(
            config=self.tasks_config["Profile_Analyst_Task"],
            output_json=CandidateProfile,
            Agent= self.Profile_Analyst_Agent,
            output_file="output/profile_analysis.json"
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
            )
from crewai import Task,Agent,Process,Crew,LLM
from crewai.project import CrewBase,agent,task,crew
from Scheme import CandidateProfile,KeywordStrategy,JobDiscoveryOutput,JobScraperOutput
from Tools import github_profile_tool,Linked_in_Profile_Tool,Job_Search_Tool,scrape_job_Tool
from dotenv import load_dotenv
from Guardrails import freshness_guardrail
import os
import agentops

load_dotenv()
llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2,
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
    @agent
    def Keyword_Strategist_Agent(self)->Agent:
        return Agent(
            config = self.agents_config["Keyword_Strategist_Agent"],
            llm = llm,
            verbose =True
        )
    
    @agent
    def Job_Search_Agent(self)->Agent:
        return Agent(
            config = self.agents_config["Job_Search_Agent"],
            llm = llm,
            tools = [Job_Search_Tool],
            verbose =True
        )
    
    @agent
    def Job_Scraper_Agent(self)->Agent:
        return Agent(
            config = self.agents_config["Job_Scraper_Agent"],
            llm = llm,
            tools = [scrape_job_Tool],
            verbose =True
        )

    @task
    def Profile_Analyst_Task(self)->Task:
        return Task(
            config=self.tasks_config["Profile_Analyst_Task"],
            agent= self.Profile_Analyst_Agent(),
            output_file="output/profile_analysis.json",
            output_json=CandidateProfile
        )

    
    @task
    def Keyword_Strategist_Task(self)->Task:
        return Task(
            config=self.tasks_config["Keyword_Strategist_Task"],
            agent=self.Keyword_Strategist_Agent(),
            output_file="output/Search_Keyword.json",
            output_json=KeywordStrategy,
            context=[self.Profile_Analyst_Task()]
        )

    
    @task 
    def Job_Search_Task(self)->Task:
        return Task(
            config=self.tasks_config["Job_Search_Task"],
            agent = self.Job_Search_Agent(),
            output_file="output/search_job_output.json",
            output_json=JobDiscoveryOutput,
            context=[self.Keyword_Strategist_Task()]
        )
    
    @task 
    def Job_Scraper_Task(self)->Task:
        return Task(
            config=self.tasks_config["Job_Scraper_Task"],
            agent = self.Job_Scraper_Agent(),
            output_file="output/scrap_job_output.json",
            output_json=JobScraperOutput,
            context=[self.Job_Search_Task()],
        )

    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
            )
    
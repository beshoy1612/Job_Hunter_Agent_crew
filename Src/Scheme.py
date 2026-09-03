from pydantic import BaseModel, Field
from typing import List, Optional


class CandidateProfile(BaseModel):

    professional_summary: str = Field(...,description="A concise summary of the candidate's professional background.")

    technical_skills: List[str] = Field(...,description="Technical skills explicitly identified from the candidate's sources.")

    programming_languages: List[str] = Field(..., description="Programming languages the candidate has experience with.")

    frameworks_and_technologies: List[str] = Field(...,escription="Frameworks, libraries, platforms, and technologies used by the candidate.")

    professional_experience: List[str] = Field(...,description="Relevant professional experience and roles.")

    education: List[str] = Field(...,description="Educational background.")

    projects: List[str] = Field(..., description="Relevant projects and the skills or technologies demonstrated by them.")

    suitable_job_roles: List[str] = Field(...,description="Job roles that best match the candidate's background and skills.")

    experience_level: str = Field(...,description="Estimated experience level such as Intern, Junior, Mid-level, or Senior.")

    key_strengths: List[str] = Field(...,description="The candidate's strongest qualifications and competitive advantages.")

    certifications: Optional[List[str]] = Field(default=None,description="Relevant certifications and training, if available.")

    github_evidence: Optional[List[str]] = Field(default=None,description="Technical skills and experience supported by the candidate's GitHub profile, if available.")

    linkedin_evidence: Optional[List[str]] = Field(default=None,description="Professional information supported by the candidate's LinkedIn profile, if available.")

    career_interests: Optional[List[str]] = Field(default=None,description="Potential career directions based on the candidate's profile, if identifiable.")

    preferred_locations: Optional[List[str]] = Field(default=None,description="Preferred job locations, if available.")

    skill_gaps: Optional[List[str]] = Field(default=None,description="Skills that may need improvement for the candidate's target roles, if identifiable." )


class KeywordStrategy(BaseModel):
    search_queries: list[str] = Field(description="Ready-to-use search queries for job-search platforms.")


class JobDiscovery(BaseModel):

    title: Optional[str] = Field(default=None, description="Title returned by the search result")
    url: str = Field(description="URL of the discovered job listing")

    content: Optional[str] = Field(default=None,description="Content snippet returned by the search engine")

    source: str = Field(description="Website where the job was discovered")


class JobDiscoveryOutput(BaseModel):

    jobs: list[JobDiscovery] = Field(default_factory=list,description="List of discovered job listings")

    

class ScrapedJob(BaseModel):
    title: str = Field(description="Verified job title.")
    company: str = Field(description="Company name.")
    location: Optional[str] = Field(default=None, description="Job location exactly as stated by the source.")
    work_mode: Optional[str] = Field(default=None, description="Work mode as explicitly stated by the source, such as Remote, Hybrid, or On-site.")
    description: str = Field(description="Brief verified summary of the job description.")
    requirements: List[str] = Field(default_factory=list, description="Verified job requirements.")
    technologies: List[str] = Field(default_factory=list, description="Technologies, tools, or skills mentioned in the job listing.")
    experience_level: Optional[str] = Field(default=None, description="Experience level required for the job.")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score between 0 and 1 based on the candidate profile.")
    source_url: str = Field(description="URL of the verified job listing.")
    application_url: Optional[str] = Field(default=None, description="Direct job application URL if available.")
    source_website: str = Field(description="Website where the job listing was found.")


class JobScraperOutput(BaseModel):
    jobs: List[ScrapedJob] = Field(default_factory=list, description="All verified job opportunities that passed the relevance threshold.")
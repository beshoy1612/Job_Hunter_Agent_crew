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
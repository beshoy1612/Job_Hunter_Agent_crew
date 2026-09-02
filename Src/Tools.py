from crewai.tools import tool
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv("GITHUB_API_KEY")
bright_data_token = os.getenv("BRIGHT_API_KEY")

@tool
def github_profile_tool(username: str) -> dict:
    """
    Fetch relevant public information from a GitHub profile.
    """

    

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    profile_response = requests.get(
        f"https://api.github.com/users/{username}",
        headers=headers
    )

    repos_response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers=headers
    )

    if profile_response.status_code != 200:
        return {
            "error": f"Could not find GitHub user: {username}"
        }

    profile = profile_response.json()
    repos = repos_response.json()

    return {
        "username": profile.get("login"),
        "name": profile.get("name"),
        "bio": profile.get("bio"),
        "location": profile.get("location"),
        "public_repositories": profile.get("public_repos"),
        "followers": profile.get("followers"),
        "repositories": [
            {
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "topics": repo.get("topics", []),
                "stars": repo.get("stargazers_count"),
                "url": repo.get("html_url")
            }
            for repo in repos
        ]
    }

@tool
def Linked_in_Profile_Tool(profile_url: str) -> dict:
    """
    Fetch public information from a LinkedIn profile using Bright Data's
    LinkedIn people scraper (synchronous mode).
    """

    dataset_id = "gd_l1viktl72bvl7bjuj0"  # LinkedIn people profiles 

    headers = {
        "Authorization": f"Bearer {bright_data_token}",
        "Content-Type": "application/json"
    }

    payload = [{"url": profile_url}]

    params = {
        "dataset_id": dataset_id,
        "notify": "false",
        "include_errors": "true"
    }

    response = requests.post(
        "https://api.brightdata.com/datasets/v3/scrape",
        headers=headers,
        params=params,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        return {
            "error": f"Could not fetch LinkedIn profile: {profile_url}",
            "status_code": response.status_code,
            "details": response.text
        }

    data = response.json()

    # Bright Data synchronous mode returns a list of records
    if isinstance(data, list) and len(data) > 0:
        record = data[0]
    else:
        record = data

    return {
        "name": record.get("name"),
        "position": record.get("position"),
        "about": record.get("about"),
        "location": record.get("city") or record.get("location"),
        "current_company": record.get("current_company_name") or record.get("current_company"),
        "experience": record.get("experience", []),
        "education": record.get("education", []),
        "skills": record.get("skills", []),
        "followers": record.get("followers"),
        "connections": record.get("connections"),
        "url": record.get("url") or profile_url
    }

from crewai.tools import tool
from dotenv import load_dotenv
from apify_client import ApifyClient
from tavily import TavilyClient
from urllib.parse import urlparse
from scrapegraph_py import Client
import requests
import os

load_dotenv()
token = os.getenv("GITHUB_API_KEY")
search_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
scrap_client = Client(api_key=os.getenv("ScrapGraphAI_API_KEY"))

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

def normalize_linkedin_url(url: str) -> str:
    """
    Normalize LinkedIn profile URLs so duplicate URLs
    can be detected.
    """

    parsed = urlparse(url)

    path = parsed.path.rstrip("/")

    # Remove trailing slashes and query parameters
    return f"https://www.linkedin.com{path}".lower()


def is_linkedin_profile(url: str) -> bool:
    """
    Check whether a URL is a LinkedIn personal profile.
    """

    if not url:
        return False

    url = url.lower()

    return (
        "linkedin.com/in/" in url
        and "/pub/dir/" not in url
        and "/jobs/" not in url
        and "/company/" not in url
    )


@tool
def Linked_in_Profile_Tool(profile_url: str) -> dict:
    """
    Find publicly available information about a specific LinkedIn profile
    using Tavily and return a clean structured JSON object.

    The tool:
    - Searches LinkedIn using Tavily.
    - Filters out non-profile pages.
    - Removes duplicate profiles.
    - Prioritizes the requested profile URL.
    - Returns clean profile information for the Profile Analyst Agent.
    """

    try:

        # ---------------------------------------------------------
        # 1. Extract LinkedIn username
        # ---------------------------------------------------------

        parsed_url = urlparse(profile_url)

        username = parsed_url.path.strip("/").split("/")[-1]

        if not username:
            return {
                "success": False,
                "error": "Invalid LinkedIn profile URL.",
                "profile_url": profile_url
            }

        # ---------------------------------------------------------
        # 2. Search specifically for this LinkedIn profile
        # ---------------------------------------------------------

        query = (
            f'site:linkedin.com/in/ '
            f'"{username}"'
        )

        response = search_client.search(
            query=query,
            search_depth="advanced",
            max_results=10,
            include_domains=["linkedin.com"],
            include_answer=True,
            include_raw_content=True
        )

        results = response.get("results", [])

        # ---------------------------------------------------------
        # 3. Keep only LinkedIn personal profiles
        # ---------------------------------------------------------

        profile_results = []

        for result in results:

            url = result.get("url", "")

            if not is_linkedin_profile(url):
                continue

            profile_results.append(result)

        # ---------------------------------------------------------
        # 4. Remove duplicate profiles
        # ---------------------------------------------------------

        unique_profiles = {}

        for result in profile_results:

            normalized_url = normalize_linkedin_url(
                result.get("url", "")
            )

            if normalized_url not in unique_profiles:

                unique_profiles[normalized_url] = result

        profile_results = list(unique_profiles.values())

        # ---------------------------------------------------------
        # 5. If no profile found
        # ---------------------------------------------------------

        if not profile_results:

            return {
                "success": False,
                "error": "No matching LinkedIn profile found.",
                "profile_url": profile_url,
                "username": username
            }

        # ---------------------------------------------------------
        # 6. Try to identify the requested profile
        # ---------------------------------------------------------

        requested_url = normalize_linkedin_url(profile_url)

        selected_profile = None

        for profile in profile_results:

            result_url = normalize_linkedin_url(
                profile.get("url", "")
            )

            if result_url == requested_url:

                selected_profile = profile
                break

        # ---------------------------------------------------------
        # 7. Fallback to the most relevant result
        # ---------------------------------------------------------

        if selected_profile is None:

            selected_profile = profile_results[0]

        # ---------------------------------------------------------
        # 8. Extract clean information
        # ---------------------------------------------------------

        title = selected_profile.get("title", "")

        content = selected_profile.get(
            "raw_content"
        ) or selected_profile.get(
            "content"
        ) or ""

        description = selected_profile.get(
            "description",
            ""
        )

        # ---------------------------------------------------------
        # 9. Return clean structured output
        # ---------------------------------------------------------

        return {
            "success": True,

            "profile": {
                "name": title.split(" - ")[0].strip()
                if title
                else None,

                "headline": title,

                "about": description,

                "url": selected_profile.get(
                    "url"
                ),

                "content": content
            },

            "search_metadata": {
                "query": query,
                "profiles_found": len(profile_results),
                "duplicates_removed": (
                    len(profile_results)
                    - len(unique_profiles)
                )
            }
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "profile_url": profile_url
        }
@tool
def Job_Search_Tool(search_queries: list[str],websites: list[str],max_job_age_days: int) -> list[dict]:
    """
    Search for recent job opportunities using Tavily.

    The search is restricted to the websites provided by the user.
    """

    jobs = []

    for query in search_queries:
        for website in websites:

            search_query = f"site:{website} {query}"

            response = search_client.search(
                query=search_query,
                search_depth="advanced",
                max_results=5,
                days=max_job_age_days
            )

            for result in response.get("results", []):
                jobs.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "content": result.get("content"),
                    "source": website
                })

    return jobs


@tool
def scrape_job_Tool(url: str) -> dict:
    """
    Extract structured information from a job listing page.
    """

    prompt = """
    Extract the following information from this job listing:

    - title
    - company
    - location
    - work_mode
    - posted_date
    - job_status
    - description
    - requirements
    - technologies
    - experience_level
    - application_url

    Return the result as structured JSON.

    Rules:

    - Do not invent information.
    - If information is not available, return null.
    - posted_date must be the original job posting date.
    - Do not use the page update date as posted_date.
    - Do not use today's date as posted_date.
    - If the original posting date cannot be verified, return null.
    - job_status should be active, expired, closed, or null.
    - Only identify a job as remote when the job listing explicitly
      states that remote work is supported.
    """

    result = scrap_client.smartscraper(
        website_url=url,
        user_prompt=prompt
    )

    return result
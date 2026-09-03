from pypdf import PdfReader
from Crew.Discovery_Crew import Discovery_crew

def extract_cv_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def run():
    cv_text = extract_cv_text(r"F:\Job_Hunter_Agent_Crew\Knowledge\Beshoy Karam cv.pdf")

    inputs = {
        "cv": cv_text,
        "github_link": "https://github.com/beshoy1612",
        "linkedin_link": "https://www.linkedin.com/in/beshoy-karam/",
        "websites":["https://www.linkedin.com/jobs","https://wuzzuf.net"],
        "relevance_threshold":0.8,
        "max_job_age_days": 30
    }

    result = Discovery_crew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()

    #"https://eg.indeed.com","https://www.glassdoor.com","https://forasna.com","https://www.akhtaboot.com","https://www.tanqeeb.com","https://www.gulftalent.com","https://www.jobzella.com" ,,"https://remoteok.com","https://weworkremotely.com"
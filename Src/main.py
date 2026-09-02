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
        "linkedin_link": "https://www.linkedin.com/in/beshoy-karam/"
    }

    result = Discovery_crew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()
from datetime import datetime


def freshness_guardrail(output):

    MAX_JOB_AGE_DAYS = 30

    valid_jobs = []

    today = datetime.now().date()

    for job in output.pydantic.jobs:

        if not job.posted_date:
            continue

        try:
            posted_date = datetime.fromisoformat(
                job.posted_date
            ).date()
        except ValueError:
            continue

        age = (today - posted_date).days

        if age < 0 or age > MAX_JOB_AGE_DAYS:
            continue

        if job.job_status:
            status = job.job_status.lower()

            if status in ["expired", "closed", "filled", "inactive"]:
                continue

        valid_jobs.append(job)

    output.pydantic.jobs = valid_jobs

    return True, output
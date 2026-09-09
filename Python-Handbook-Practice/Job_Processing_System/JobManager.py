from dataclasses import dataclass 
from Job import Job

class JobManager:
    jobs: list[Job]

    def __init__(self):
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)

    def remove_job(self, job_id):
        filtered_job = [job for job in self.jobs if job.id != job_id]
        self.jobs = filtered_job

    def get_job(self, job_id):
        find_job = [job for job in self.jobs if job.id == job_id]
        if len(find_job) > 0:
            return find_job[0] 
        else:
            return None

    def __len__(self):
        return len(self.jobs)

    def __str__(self):
        return self.jobs

    def __repr__(self):
            return self.jobs
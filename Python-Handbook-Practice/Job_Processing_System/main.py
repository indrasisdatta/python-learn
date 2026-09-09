from Job import Job 
from JobManager import JobManager 

job1 = Job(1, 50, 'Resume for job1', 4, 'Open', '2026-06-01', 1)
job2 = Job(2, 50, 'Resume for job2', 6, 'Pending', '2026-06-02', 1)
job3 = Job(3, 50, 'Resume for job3', 3, 'Open', '2026-06-03', 1)
job4 = Job(4, 96, 'Resume for job4', 2, 'Processing', '2026-06-05', 1)
job5 = Job(5, 96, 'Resume for job5', 1, 'Open', '2026-06-13', 1)
job6 = Job(6, 100, 'Resume for job6', 5, 'Closed', '2026-06-21', 1)

job_manager = JobManager()

job_manager.add_job(job1)
job_manager.add_job(job2)
job_manager.add_job(job3)
job_manager.add_job(job4)
print(len(job_manager))

job_manager.remove_job(3)
job_manager.remove_job(2)
print(len(job_manager))

print(job_manager.get_job(1))

print(str(job_manager))

#TODO: 

# sort by date 

# access check
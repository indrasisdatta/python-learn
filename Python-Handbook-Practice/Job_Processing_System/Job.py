from dataclasses import dataclass

@dataclass
class Job:
    id: int 
    user_id: int 
    document: str 
    priority: int 
    status: str 
    created_at: str 
    attempts: int 



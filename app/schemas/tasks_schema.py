from pydantic import BaseModel

class InitialTask(BaseModel):
    title: str
    description: str|None = None


class UpdatedTask(BaseModel):
    title: str
    description: str|None = None
    completed: bool = None

class FullTask(BaseModel):
    id: int
    title: str
    description: str|None = None
    completed: bool = False 

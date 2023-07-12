from typing import List
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


# Staff related models

class Attribute(Enum):
    DOCTOR = "doctor"
    PHLEBOTOMIST = "phlebotomist"
    NURSE = "nurse"
    TECHNICIAN = "technician"
    RESEARCH_ASSISTANT = "research_assistant"

SkillSet = List[Attribute]

class Shift(BaseModel):
    # required breaks can be determined by the duration
    start_time: datetime
    finish_time: datetime


class StaffMember(BaseModel):
    name: str
    attributes: SkillSet
    shift: Shift

# Study related models
class Task(BaseModel):
    start_after: datetime
    finish_before: datetime
    duration: int

    blocked_by: List["Task"] = Field(default_factory=list)

    required_attributes: List[SkillSet]

    title: str

class Patient(BaseModel):
    name: str
    tasks: List[Task]
    floor_number: int

class StudySchedule(BaseModel):
    patients: List[Patient]
    floor_number: int


class WorkDay(BaseModel):
    schedules: List[StudySchedule]
    staff: List[StaffMember]


# Solution related models
class Solution(BaseModel):
    allocations: None


# Other considerations
# Continuity of tasks per staff member

from typing import List, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


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
    #shift: Shift


class TaskType(Enum):   #KEY WORDS:
    DOCTOR = 1          #EXAM, EXAMINATION, PHYSICAL, DOCTOR, ELIGIBILITY
    NURSE = 2           #DOSE, PREDOSE, AE, ADVERSE, MEDICATION, ASSESS, SITE, ACCOUNTABILITY, DISPENSE, REPORTED, INFUSION, MONITOR
    CRT = 3             #BREAKFAST, LUNCH, DINNER, SNACK, SUPINE, ECG, VITAL, VITALS, ASSESSMENT, COMMENCE, BLOCK, PREG, DOA, URINALYSIS, URINE, MSU, WEIGHT, BMI, ALCOHOL, CLEAN, LINEN, WALK
    PHLEBOTOMY = 4      #CANNULA, CANNULATION, BLOOD, SAFETIES, FLUSH
    SPIRO = 6           #SPIROMETRY
    SPUTUM = 7          #SPUTUM
    TRIPLICATE = 5      #TRIPLICATE --must be same staff
    PHONE = 6           #PHONE --will be in day header row
    ANY = 7             #ADMIT, WRIST, WRISTBAND, COMPLIANCE, REMIND, ENSURE, RULES, TOUR, WORKBOOK, DISCHARGE, ENCOURAGE, ORIENTATION, RESTRICTIONS
    PHARMACY = 8        #RANDOMISATION


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


class StudySchedule(BaseModel):
    patients: List[Patient]
    floor_number: int


class WorkDay(BaseModel):
    schedules: List[StudySchedule]
    staff: List[StaffMember]


# Solution related models
class Solution(BaseModel):
    allocations: List[Tuple[StaffMember, Task]]


# Other considerations
# Continuity of tasks per staff member

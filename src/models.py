from typing import List, Tuple
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


# Staff related models


class Attribute(Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    TECHNICIAN = "technician"
    PHLEBOTOMIST = "phlebotomist"


class Shift(BaseModel):
    # required breaks can be determined by the duration
    start_time: datetime
    finish_time: datetime


class TaskType(Enum):   #KEY WORDS:
    DOCTOR          = 1     #EXAM, EXAMINATION, PHYSICAL, DOCTOR, ELIGIBILITY
    NURSE           = 2     #DOSE, PREDOSE, AE, ADVERSE, MEDICATION, ASSESS, SITE, ACCOUNTABILITY, DISPENSE, REPORTED, MONITOR, PHONE
    TEAM_LEAD       = 3
    CRT             = 4     #BREAKFAST, LUNCH, DINNER, SNACK, SUPINE, ECG, VITAL, VITALS, ASSESSMENT, COMMENCE, BLOCK, PREG, DOA, URINALYSIS, URINE, MSU, WEIGHT, BMI, ALCOHOL, CLEAN, LINEN, WALK
    PHLEBOTOMY      = 5     #BLOOD, SAFETIES, FLUSH
    CANNULATION     = 6     #CANNULATION
    INFUSION        = 7     #INF, "IV ", INTRAVENOUS
    SPIRO           = 8     #SPIROMETRY
    DOMINO_SPIRO    = 9
    SPUTUM          = 10     #SPUTUM
    PORTACATH       = 11
    PAEDS_PORT      = 12
    CYTOTOXIC       = 13
    BREEZING        = 14
    TRIPLICATE      = 15     #TRIPLICATE --must be same staff
    ANY             = 16     #ADMIT, WRIST, WRISTBAND, COMPLIANCE, REMIND, ENSURE, RULES, TOUR, WORKBOOK, DISCHARGE, ENCOURAGE, ORIENTATION, RESTRICTIONS
    PHARMACY        = 17    #RANDOMISATION
    DATE            = 18    #DATE
    DAY             = 19    #DAY
    JAIPUR          = 20 
    MISSION         = 21    #STUDY_NAME=MISSION
    MISSION_ECG     = 22
    OSPREY          = 23    #ELECTROPORATION
    OTHER           = 24    #default if no keywords are found


SkillSet = List[TaskType]


class StaffMember(BaseModel):
    name: str
    shift: Shift
    attributes: SkillSet


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

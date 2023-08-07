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


class TaskType(Enum):       #KEY WORDS:
    DOCTOR          = "doctor"     #EXAM, EXAMINATION, PHYSICAL, DOCTOR, ELIGIBILITY
    NURSE           = "nurse"     #DOSE, PREDOSE, AE, ADVERSE, MEDICATION, ASSESS, SITE, ACCOUNTABILITY, DISPENSE, REPORTED, MONITOR, PHONE
    CRT             = "crt"     #BREAKFAST, LUNCH, DINNER, SNACK, MEAL, SUPINE, ECG, VITAL, VITALS, COMMENCE, BLOCK, PREG, DOA, URINALYSIS, URINE, MSU, WEIGHT, BMI, ALCOHOL, CLEAN, LINEN, WALK
    PHLEBOTOMY      = "phlebotomy"     #BLOOD, SAFETIES, FLUSH
    CANNULATION     = "cannulation"     #CANNULATION
    INFUSION        = "infusion"     #INF, "IV ", INTRAVENOUS
    SPIRO           = "spiro"     #SPIROMETRY
    DOMINO_SPIRO    = "domino_spiro"     #if STUDY_NAME=DOMINO, SPIRO, SPIROMETRY
    SPUTUM          = "sputum"     #SPUTUM
    PORTACATH       = "portacath"    #PORT,
    PAEDS_PORT      = "paeds_port"    #if STUDY_NAME=MISSION, PORT
    CYTOTOXIC       = "cytotoxic"    
    BREEZING        = "breezing"    #REE
    TRIPLICATE      = "triplicate"    #TRIPLICATE --must be same staff
    ANY             = "any"    #ADMIT, WRIST, WRISTBAND, COMPLIANCE, REMIND, ENSURE, RULES, TOUR, WORKBOOK, DISCHARGE, ENCOURAGE, ORIENTATION, RESTRICTIONS
    PHARMACY        = "pharmacy"    #RANDOMISATION
    DATE            = "date"    #DATE
    DAY             = "day"    #DAY
    JAIPUR          = "jaipur"    #if STUDY_NAME=JAIPUR, DOSE
    MISSION         = "mission"    #STUDY_NAME=MISSION
    MISSION_ECG     = "mission_ecg"    #if STUDY_NAME=MISSION, ECG
    OSPREY          = "osprey"    #ELECTROPORATION
    OTHER           = "other"    #default if no keywords are found


SkillSet = List[TaskType]


class StaffMember(BaseModel):
    name: str
    shift: Shift
    attributes: SkillSet


# Study related models
class Task(BaseModel):
    study: str
    patient: str
    start_after: datetime
    finish_before: datetime
    duration: int
    blocked_by: List["Task"] = Field(default_factory=list)
    # This is a list because some tasks may require multiple people
    required_attributes: List[SkillSet]
    title: str


class WorkDay(BaseModel):
    tasks: List[Task]
    staff: List[StaffMember]


# Solution related models
class Solution(BaseModel):
    allocations: List[Tuple[StaffMember, Task]]


# Other considerations
# Continuity of tasks per staff member

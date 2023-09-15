from typing import List, Tuple, Union
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


# Staff related models

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
    floor: str


# Study related models
class Task(BaseModel):
    study: str
    floor: str
    patient: str
    # time can be string, this is actually indicates it's none
    # TODO(o.kyle): make this only a datetime, and ignore tasks with no time
    #   It was originally str to make it easier to put into the results excel
    time: Union[datetime, str]
    #start_after: datetime
    #finish_before: datetime
    duration: int
    strict_staffing: bool   #false if the task is flexible in its staff requirements, true if it is strict
    #blocked_by: List["Task"] = Field(default_factory=list)         LATER
    # This is a list because some tasks may require multiple people
    # TODO(o.kyle): Either change this to a list of SkillSets, or decide it will remain a single SkillSet
    required_attributes: TaskType
    #required_attributes: List[SkillSet]
    title: str
    triplicate: bool
    #can this be instantiated with either set time OR start_after/finish_after?


class WorkDay(BaseModel):
    tasks: List[Task]
    staff_members: List[StaffMember]

    # TODO(o.kyle): add this here and implement in excel parser
    #   Ideally it should be the start of the day we're interested in,
    #   but it can be any time really. I will use it to count minutes from for all time
    #   values in the solver (i.e. 9am is 540 minutes from the start of the day)
    # relative_to: datetime


# Solution related models
class Solution(BaseModel):
    allocations: List[Tuple[StaffMember, Task]]


#triplicates need to be same person, if they can't do the last one they can't do the first one
#two RNs needed to dose
#If no CRTs available for task, assign RN
#If no one is available in the same floor, assign someone from other floor
#------> Task type can have a length and a "fit" (how correct the assignment has to be, i.e. phlebotomy is a 1 and meals a 0 because one requires training and the other doesnt)
#Consider task load

# Other considerations
# Continuity of tasks per staff member

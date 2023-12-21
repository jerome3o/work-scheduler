interface StudySchedule {
  name: string;
  content: File;
}

interface RosterProcessingResult {
  days: string[];
}

interface StudyScheduleProcessingResult {
  days: string[];
  cohorts: string[];
}

interface WorkDay {
  tasks: string[];
  staffMembers: string[];
}

interface StudyScheduleOptions {
  day: string;
  cohort: string;
}

interface GenerateWorkDayOptions {
  studyScheduleOptions: StudyScheduleOptions[];
  rosterDay: string;
}

export {
  type StudySchedule,
  type RosterProcessingResult,
  type StudyScheduleProcessingResult,
  type WorkDay,
  type StudyScheduleOptions,
  type GenerateWorkDayOptions,
};

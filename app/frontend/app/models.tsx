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

export {
  type StudySchedule,
  type RosterProcessingResult,
  type StudyScheduleProcessingResult,
};

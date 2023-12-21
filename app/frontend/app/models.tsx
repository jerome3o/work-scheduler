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

interface StudyScheduleInfo {
  schedule: StudySchedule;
  options: StudyScheduleProcessingResult | undefined;
}

export {
  type StudySchedule,
  type RosterProcessingResult,
  type StudyScheduleProcessingResult,
  type StudyScheduleInfo,
};

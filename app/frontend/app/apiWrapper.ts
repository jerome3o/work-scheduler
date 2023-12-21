import { RosterProcessingResult, StudyScheduleProcessingResult, WorkDay } from "./models";

export default class ApiWrapper {
    url: string;

    constructor(url: string | undefined = undefined) {
        this.url = url ?? "/api";
    }

    async processRoster(rosterFile: File): Promise<RosterProcessingResult> {
        const formData = new FormData();
        formData.append("roster_file", rosterFile, rosterFile.name);
        const response = await fetch(`${this.url}/process-files/roster`, {
            method: "POST",
            body: formData,
        });
        return await response.json();
    }

    async processStudySchedule(studyScheduleFile: File): Promise<StudyScheduleProcessingResult> {
        const formData = new FormData();
        formData.append("study_schedule_file", studyScheduleFile, studyScheduleFile.name);
        const response = await fetch(`${this.url}/process-files/study-schedule`, {
            method: "POST",
            body: formData,
        });
        return await response.json();
    }

    async generateWorkDay(
        studyScheduleFiles: File[],
        rosterFile: File,
    ): Promise<WorkDay> {
        const formData = new FormData();
        studyScheduleFiles.forEach((file) =>
            formData.append("study_schedule_files", file, file.name)
        );
        formData.append("roster_file", rosterFile, rosterFile.name);
        formData.append("additional_data", JSON.stringify({ something: "else" }));

        const response = await fetch(`${this.url}/process-files/build-workday`, {
            method: "POST",
            body: formData,
        });

        return await response.json();
    }
}

"use client"

import Uploader from "./Uploader"


export default function SchedulerApp() {
    return (
        <div className="scheduler-app-container">
            <div>
                <h1>Scheduler App</h1>
                <Uploader fileType="docx" title="Nurse Schedule"></Uploader>
                <Uploader fileType="xlsx" title="Task list"></Uploader>
                <Uploader fileType="xlsx" title="Durations"></Uploader>
                <Uploader fileType="csv" title="Jerome's just adding an example"></Uploader>
            </div>
            <div id="generate-button-div">
                <button id="generate-button">Generate</button>
            </div>
        </div>
    )
}

import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        dateObject: String,
    }

    static targets = ["timeHoursMinutes", "timeHoursMinutes2"]
    
    connect() {
        const dateObject = new Date(this.data.get("dateObjectValue"))
        const minutes = dateObject.getMinutes() < 10 ? `0${dateObject.getMinutes()}` : dateObject.getMinutes();
        const time = `${dateObject.getHours()}:${minutes}`

        this.timeHoursMinutesTarget.textContent = time
        this.timeHoursMinutes2Target.textContent = time
    }
}

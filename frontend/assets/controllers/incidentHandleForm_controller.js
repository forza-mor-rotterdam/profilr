import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        formIsSubmitted: Boolean,
        parentContext: String,
        handledOptions: String,
    }
    
    connect() {
        console.log(this.formIsSubmittedValue)
        const handledOptions = JSON.parse(this.handledOptionsValue)
        console.log(handledOptions)

        this.element.dispatchEvent(new CustomEvent("formHandleIsConnected", {
            detail: JSON.parse(this.parentContextValue),
            bubbles: true
        }));
    }
}

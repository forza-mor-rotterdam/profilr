import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        formIsSubmitted: Boolean,
        parentContext: String
    }
    
    connect() {
        console.log(this.formIsSubmittedValue)

        this.element.dispatchEvent(new CustomEvent("formHandleIsConnected", {
            detail: JSON.parse(this.parentContextValue),
            bubbles: true
        }));
    }
}

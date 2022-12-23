import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        formIsSubmitted: Boolean,
        parentContext: String,
        handledOptions: String,
    }

    static targets = ["externalText", "internalText"]
    
    connect() {
        if(this.hasExternalTextTarget) {
            if(this.externalTextTarget.textContent.length > 0) {
                this.externalMessage = this.externalTextTarget.textContent
            }
        }

        this.element.dispatchEvent(new CustomEvent("formHandleIsConnected", {
            detail: JSON.parse(this.parentContextValue),
            bubbles: true
        }));
    }

    cancelHandle() {
        this.element.dispatchEvent(new CustomEvent("cancelHandle", {
            detail: JSON.parse(this.parentContextValue),
            bubbles: true
        }));
    }

    setExternalMessage(evt){
        this.choice =  evt.params.index
        this.externalMessage = JSON.parse(this.handledOptionsValue)[this.choice][2]
        this.externalTextTarget.value = this.externalMessage
    }

    defaultExternalMessage(){
        if(this.externalMessage.length === 0) return
        
        this.externalTextTarget.value = this.externalMessage
    }

    clearExternalMessage() {
        this.externalTextTarget.value = ""
    }
}

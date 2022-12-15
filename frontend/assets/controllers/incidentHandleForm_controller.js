import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        formIsSubmitted: Boolean,
        parentContext: String,
        handledOptions: String,
    }
    static targets = ["externalText", "internalText"]
    
    connect() {
        console.log('CONNECT, this.externalTextTarget', this.externalTextTarget)
        if(this.externalTextTarget !== undefined) {
            if(this.externalTextTarget?.textContent.length > 0) {
                this.externalMessage = this.externalTextTarget.textContent
            }
        }

        this.element.dispatchEvent(new CustomEvent("formHandleIsConnected", {
            detail: JSON.parse(this.parentContextValue),
            bubbles: true
        }));
    }

    setExternalMessage(evt){
        this.choice =  evt.params.index
        this.externalMessage = JSON.parse(this.handledOptionsValue)[this.choice][2]
        this.externalTextTarget.textContent = this.externalMessage
    }

    defaultExternalMessage(){
        if(this.externalMessage.length === 0) return
        
        this.externalTextTarget.textContent = this.externalMessage
    }

    clearExternalMessage() {
        this.externalTextTarget.textContent = ""
    }

}

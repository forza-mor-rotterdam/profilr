import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = [ "groupList", "subjectList" ]
    static values = {
        groupList: String,
        groupSelected: String
    }
    

    connect() {
        const groupOptions = JSON.parse(this.groupListValue)
        
        for(let i = 0; i < groupOptions.length; i++) {
            const opt = groupOptions[i];
            const el = document.createElement("option");
            if(opt.value === this.groupSelectedValue) {
                el.selected = true;
            }
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.groupListTarget.appendChild(el);
        }
        this.setSubjects()
    }

    initialize() {
        
    }

    setSubjects(event) {
        const groupOptions = JSON.parse(this.groupListValue)
        const selectedValue = event !== undefined ? event.target.value : "1"
        const subject = groupOptions.find(subject => subject.code === selectedValue)
        const subjectOptions = subject.onderwerpen
        
        for (const option of document.querySelectorAll('#subjectList > option')) {
            option.remove();
        }

        for(let i = 0; i < subjectOptions.length; i++) {
            const opt = subjectOptions[i];
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.subjectListTarget.appendChild(el);    
        }
    }
}

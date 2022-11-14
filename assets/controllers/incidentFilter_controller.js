import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = [ "areaList", "districtList", "departmentList" ]
    static values = {
        areaList: String,
        departmentList: String,
        areaSelected: String
    }
    

    connect() {
        const areaOptions = JSON.parse(this.areaListValue)
        for(let i = 0; i < areaOptions.length; i++) {
            const opt = areaOptions[i];
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.areaListTarget.appendChild(el);
        }

        const departmentsOptions = JSON.parse(this.departmentListValue)
        
        const instruction = document.createElement("option");
        instruction.setAttribute('disabled', 'disabled');
        instruction.setAttribute('selected', 'selected');
        instruction.setAttribute('hidden', 'hidden');
        instruction.textContent = 'Selecteer een afdeling';
        this.departmentListTarget.appendChild(instruction);
            
        for(let i = 0; i < departmentsOptions.length; i++) {
            const opt = departmentsOptions[i];
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.departmentListTarget.appendChild(el);
        }

        this.setDistrict()

    }

    setDistrict(event) {
        const areaOptions = JSON.parse(this.areaListValue)
        const selectedValue = event !== undefined ? event.target.value : "1"
        // const selectedValue = event.target.value
        const district = areaOptions.find(district => district.code === selectedValue)
        const districtOptions = district.buurten
        
        for (const option of document.querySelectorAll('#buurten > option')) {
            option.remove();
        }

        for(let i = 0; i < districtOptions.length; i++) {
            const opt = districtOptions[i];
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.districtListTarget.appendChild(el);    
        }
    }
}

import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = [ "areaList", "districtList", "departmentList" ]
    static values = {
        areaList: String,
        departmentList: String,
        areaSelected: String
    }
    

    connect() {
        console.log(this.departmentListValue)
        const departmentsOptions = JSON.parse(this.departmentListValue)
        console.log(departmentsOptions.length);
        // console.log(this.areaListValue)
        const areaOptions = JSON.parse(this.areaListValue);
        console.log(areaOptions.length);
        for(let i = 0; i < areaOptions.length; i++) {
            const opt = areaOptions[i];
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.areaListTarget.appendChild(el);
        }

        console.log(departmentsOptions.length);
        
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
        const selectedValue = event !== undefined ? event.target.value : "26"
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

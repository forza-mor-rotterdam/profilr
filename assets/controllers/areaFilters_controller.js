import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = [ "areaList", "districtList" ]
    static values = {
        areaList: String,
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
        this.setDistrict()
    }

    initialize() {
        
    }

    setDistrict(event) {
        console.log('event', event)
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
            console.log('option', opt)
            const el = document.createElement("option");
            el.textContent = opt.omschrijving;
            el.value = opt.code;
            this.districtListTarget.appendChild(el);    
        }
    }
}

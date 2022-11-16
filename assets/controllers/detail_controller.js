import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        areaList: String,
        currentDistrict: String
    }
    static targets = ['area', 'district']
    
    connect() {
        if(this.currentDistrictValue) {
            let currentArea = JSON.parse(this.areaListValue).find(area => area.buurten.some((district) => district.code === this.currentDistrictValue))
            this.areaTarget.textContent = currentArea.omschrijving
            this.districtTarget.textContent = currentArea.buurten.find((district) => district.code === this.currentDistrictValue).omschrijving
        } else {
            this.areaTarget.textContent = '-'
            this.districtTarget.textContent = '-'
        }
    }
}

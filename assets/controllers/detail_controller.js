import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        areaList: String,
        currentDistrict: String
    }
    static targets = ['area', 'district', 'selectedImage', 'thumbList']
    
    connect() {
        if(this.currentDistrictValue) {
            let currentArea = JSON.parse(this.areaListValue).find(area => area.buurten.some((district) => district.code === this.currentDistrictValue))
            this.areaTarget.textContent = currentArea.omschrijving
            this.districtTarget.textContent = currentArea.buurten.find((district) => district.code === this.currentDistrictValue).omschrijving
        } else {
            this.areaTarget.textContent = '-'
            this.districtTarget.textContent = '-'
        }
        if(this.hasThumbListTarget) {
            this.thumbListTarget.getElementsByTagName('li')[0].classList.add('selected')
        }
    }

    selectImage(e) {
        
        const imgSrc = e.params.imageSource;
        this.selectedImageTarget.src = imgSrc;

        this.deselectThumbs(e.target.closest('ul'));
        e.target.closest('li').classList.add('selected')
    }

    deselectThumbs(list) {
        for (const item of list.querySelectorAll('li')) {
            item.classList.remove('selected');
        }
    }
}

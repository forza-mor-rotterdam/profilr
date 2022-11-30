import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        areas: String,
        filters: String
    }

    connect() {
        const filterAreaList = JSON.parse(this.filtersValue).wijken ?? []
        const filterDistrictList = JSON.parse(this.filtersValue).buurten ?? []
        const areaCheckList = Array.from(document.getElementsByClassName('filter--area'))
        areaCheckList.forEach(check => {
            if(filterAreaList.find(area => area[0] === check.value)) {
                check.checked = true
                //open nested districts
                check.closest('.container__check-area')
                    .getElementsByClassName('container__list--districts')[0]
                    .classList.remove('hidden')

                // check districts
                const districtCheckList = Array.from(check.closest('.container__check-area')
                    .getElementsByClassName('filter--district'))
                
                districtCheckList.forEach(check => {
                    if(filterDistrictList.find(district => district[0] === check.value)) {
                        check.checked = true
                    }
                })
            }
        })
    }
    
    toggleArea(e) {
        const districts = e.target.closest('li').getElementsByClassName('container__list--districts')[0]
        if(e.target.checked) {
            districts.classList.remove('hidden')
        } else {
            const list = [].slice.call(districts.getElementsByTagName('input'))
            list.forEach(input => {
                input.checked = false
            });
            districts.classList.add('hidden')
        }
    }

    selectAreaFromDistrict(e) {
        const area = e.target.closest('.container__check-area').getElementsByTagName('input')[0]
        area.checked = true;
    }
}

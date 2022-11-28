import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
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

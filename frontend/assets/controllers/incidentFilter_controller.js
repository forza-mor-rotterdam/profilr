import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    initialize() {
        this.openModal()
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

    openModal() {
        const modal = document.getElementById('modal-filter');
        const modalBackdrop = document.getElementById('modal-backdrop');
            
        document.body.classList.add('show-modal');
        const exits = modal.querySelectorAll('.modal-exit');
        exits.forEach(function (exit) {

            exit.addEventListener('click', function (event) {
                event.preventDefault();
                modal.classList.remove('show');
                modalBackdrop.classList.remove('show');
                document.body.classList.remove('show-modal');
            });
        });
    }
}

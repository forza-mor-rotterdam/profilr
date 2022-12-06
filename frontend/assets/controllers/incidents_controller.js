import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        filters: String
    }

    // initialize() {
    //     const departments = JSON.parse(this.filtersValue).afdelingen

    //     if(departments?.length > 0) {
    //         //show incidents
    //     } else {
    //         this.openFilterModal()
    //     }
    // }

    openFilterModal() {
        const modal = document.getElementById('modal-filter--first');
        const modalBackdrop = document.getElementById('modal-backdrop');

        document.body.classList.add('show-modal--first-filter');
        const exits = modal.querySelectorAll('.modal-exit');
        exits.forEach(function (exit) {

            exit.addEventListener('click', function (event) {
                event.preventDefault();
                modal.classList.remove('show');
                modalBackdrop.classList.remove('show');
                document.body.classList.remove('show-modal--first-filter');
            });
        });
    }
}

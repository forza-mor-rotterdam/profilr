import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    static targets =['countActiveFilter']

    initialize() {
        this.countActiveFilterTarget.textContent=document.getElementsByClassName('js-filter-active').length
    }

    showFilters(e) {
        document.body.classList.add('show-filters')
    }

    hideFilters(e) {
        document.body.classList.remove('show-filters')
    }

    removeFilter(e) {
        e.preventDefault()
        const input = document.querySelector(`[name="${e.params.description}"][value="${e.params.code}"]`);
        input.checked = false;
        document.getElementById('incidentFilterAllForm').submit()
    }
}

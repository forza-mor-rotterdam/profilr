import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    // static targets =['countActiveFilter']

    showFilters(e) {
        document.body.classList.add('show-filters')
    }

    hideFilters(e) {
        document.body.classList.remove('show-filters')
    }

    removeFilter(e) {
        // e.preventDefault()
        // document.body.classList.add('show-spinner')
        const input = document.querySelector(`[name="${e.params.description}"][value="${e.params.code}"]`);
        input.checked = false;
        document.getElementById('incidentFilterAllForm').requestSubmit()
    }
    toggleActiveFilter(e) {
        e.preventDefault()
        const input = document.querySelector(`[name=active_filter_open]`);
        input.value = e.target.hasAttribute("open")
    }
    submitFilter() {
        const frame = document.getElementById('incidents_list');
        frame.reload()
        this.hideFilters()
    }
}

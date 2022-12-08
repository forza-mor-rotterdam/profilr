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
        const input = document.querySelector(`[name=foldout_states]`);
        let idArray = JSON.parse(input.value)
        const idAttr = e.target.getAttribute("id")
        const isOpen = e.target.hasAttribute("open")
        let index = idArray.indexOf(idAttr)
        if (index > -1) {
            idArray.splice(index, 1); 
        }
        if (isOpen){
            idArray.push(idAttr);
        }
        input.value = JSON.stringify(idArray)
    }

    onChangeFilter() {
        document.getElementById('incidentFilterAllForm').requestSubmit()    
    }

    onSubmitFilter() {
        const frame = document.getElementById('incidents_list');
        frame.reload()
        this.hideFilters()
    }
}

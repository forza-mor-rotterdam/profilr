import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    showFilters() {
        document.body.classList.add('show-filters')
    }

    hideFilters() {
        document.body.classList.remove('show-filters')
    }

    removeFilter(e) {
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
        console.log('onSubmitFilter')
        const frame = document.getElementById('incidents_list');
        frame.reload()
        this.hideFilters()
    }

    selectAll(e) {
        const checkList = Array.from(e.target.closest('details').querySelectorAll('.form-check-input'))
        const doCheck = e.params.filterType === 'all' 
        checkList.forEach(element => {
            element.checked = doCheck
        });
    }

    removeAllFilters(e) {
        const checkedFilters = Array.from(document.getElementsByClassName(`btn-filter--active`));
        checkedFilters.forEach(filter => {
            const input = document.querySelector(`[name="${filter.getAttribute('data-filter--filter-description-param')}"][value="${filter.getAttribute('data-filter--filter-code-param')}"]`);
            input.checked = false;
        })
        document.getElementById('foldout_active_filters').removeAttribute('open');
        document.getElementById('incidentFilterAllForm').requestSubmit();
        const input = document.querySelector(`[name=foldout_states]`);
        let idArray = JSON.parse(input.value)
        let index = idArray.indexOf('foldout_active_filters')
        if (index > -1) {
            idArray.splice(index, 1); 
        }
        input.value = JSON.stringify(idArray)
    }
}

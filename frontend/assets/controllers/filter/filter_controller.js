import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    connect() {
        
    }

    showFilters(e) {
        console.log('show filters')
        document.body.classList.add('show-filters')
    }

    hideFilters(e) {
        console.log('hide filters')
        document.body.classList.remove('show-filters')
    }

    removeFilter(e) {
        e.preventDefault()
        console.log('removeFIlter')
    }

}

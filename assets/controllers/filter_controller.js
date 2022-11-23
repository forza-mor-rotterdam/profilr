import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    

    connect() {
        console.log('connect flters')
    }

    showFilters(e) {
        console.log('show')
        document.body.classList.add('show-filters')
    }

    hideFilters(e) {
        console.log('hide')
        document.body.classList.remove('show-filters')
    }

}

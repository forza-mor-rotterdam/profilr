import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        filters: String
    }

    connect() {
        
    }

    submitFilter() {
        document.getElementById('incidentFilterAllForm').requestSubmit()    
    }
}

import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        filters: String
    }

    connect() {
        
    }

    submitFilter() {
        document.getElementById('incidentFilterAllForm').requestSubmit()
        const frame = document.querySelector('turbo-frame#incidents_list')
        
        //als data binnen is, reload frame        
        setTimeout(() => {
            frame.reload()
        }, 1000)
        
    }
}

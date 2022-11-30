import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = [ "input", "toggle" ]

    toggle(e) {
        let type = this.inputTarget.getAttribute('type') === 'password' ? 'text' : 'password';
        this.inputTarget.setAttribute('type', type);
        this.toggleTarget.classList.toggle('password__toggle-active');
    }

    submitLogin() {
        document.body.classList.add('show-spinner')
    }
}

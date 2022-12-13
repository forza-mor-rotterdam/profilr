import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = ["button"]
    connect() {
    }

    formHandleIsConnectedHandler(event) {
        const removeElem = this.element.parentNode;
        if (event.detail.is_handled){
            this.element.classList.add("hide");
            this.element.addEventListener('transitionend', function(e){
                removeElem.parentNode.removeChild(removeElem);
            });
            const btn = this.element.querySelector("button");
            console.log(btn)
            this.buttonTarget.textContent = event.detail.messages.join(",")
        }
    }

    swipe(e) {
        const li = e.target.tagName.toLowerCase() !== "img" && e.target.closest("li");
        const btn = e.target.closest("button");
        const anchor = e.target.closest("div.background-image")
        if(!anchor){
            if (li && li.scrollLeft === 0) {
                li.scrollBy({
                left: 1,
                behavior: "smooth"
                });
            } else if (!btn && li) {
                li.scrollBy({
                left: -1,
                behavior: "smooth"
                });
            } else if (btn && li) {
                // window.location.href=`/incident/${this.idValue}/handle`;
                li.scrollBy({
                    left: -1,
                    behavior: "smooth"
                });
            }
        }
    }

    openModal(e) {
        const data = e.params.object;
        const frame = e.target.closest('turbo-frame');
        const modal = frame.querySelector('.modal');
        const modalBackdrop = frame.querySelector('.modal-backdrop');

        console.log(modal)

        modal.setAttribute('data-id', data.id);
        modal.setAttribute('data-subjectId', data.onderwerp.id);
        // modal.querySelector('[data-address]').textContent= `${data.locatie.adres.straatNaam}${' '}${data.locatie.adres.huisnummer} `;


        modal.classList.add('show');
        modalBackdrop.classList.add('show');
        document.body.classList.add('show-modal');
        const exits = modal.querySelectorAll('.modal-exit');
        exits.forEach(function (exit) {

            exit.addEventListener('click', function (event) {
                event.preventDefault();
                modal.classList.remove('show');
                modalBackdrop.classList.remove('show');
                document.body.classList.remove('show-modal');
            });
        });
    }
}

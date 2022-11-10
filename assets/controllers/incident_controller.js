import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        id: String
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
                window.location.href=`/incident/${this.idValue}/handle`;
                li.scrollBy({
                    left: -1,
                    behavior: "smooth"
                });
            }
        }
    }
}

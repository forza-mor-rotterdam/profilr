import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = ["button", "turboFormHandler"]
    connect() {
        const frame = this.element.closest("turbo-frame")
        this.initialTouchPos = null
        this.bindStart = this.handleGestureStart.bind(this);
        this.bindMove = this.handleGestureMove.bind(this);
        this.bindEnd = this.handleGestureEnd.bind(this);
        this.addAllListeners()
    }

    addAllListeners() {
         // Check if pointer events are supported.
         if (window.PointerEvent) {
            // Add Pointer Event Listener
            this.element.addEventListener('pointerdown', this.bindStart);
            this.element.addEventListener('pointermove', this.bindMove);
            this.element.addEventListener('pointerup', this.bindEnd);
            this.element.addEventListener('pointercancel', this.bindEnd);
        } else {
            // Add Touch Listener
            this.element.addEventListener('touchstart', this.bindStart);
            this.element.addEventListener('touchmove', this.bindMove);
            this.element.addEventListener('touchend', this.bindEnd);
            this.element.addEventListener('touchcancel', this.bindEnd);
            // Add Mouse Listener
            this.element.addEventListener('mousedown', this.bindStart);
        }
    }

    removeAllListeners() {
        // Check if pointer events are supported.
        if (window.PointerEvent) {
           // Add Pointer Event Listener
           this.element.removeEventListener('pointerdown', this.bindStart);
           this.element.removeEventListener('pointermove', this.bindMove);
           this.element.removeEventListener('pointerup', this.bindEnd);
           this.element.removeEventListener('pointercancel', this.bindEnd);
       } else {
           // Add Touch Listener
           this.element.removeEventListener('touchstart', this.bindStart);
           this.element.removeEventListener('touchmove', this.bindMove);
           this.element.removeEventListener('touchend', this.bindEnd);
           this.element.removeEventListener('touchcancel', this.bindEnd);
           // Add Mouse Listener
           this.element.removeEventListener('mousedown', this.bindStart);
       }
   }

    formHandleIsConnectedHandler(event) {
        const removeElem = this.element.parentNode;
        if (event.detail.is_handled){
            this.element.classList.add("hide");
            // TODO toon tekst in de melding
            this.element.addEventListener('transitionend', function(e){
                removeElem.parentNode?.removeChild(removeElem);
            });
            this.buttonTarget.textContent = event.detail.messages.join(",")
        }
    }

    cancelHandleHandler(event) {
        this.closeModal()
    }

    // Handle the start of gestures
    handleGestureStart(evt) {
        evt.preventDefault();
        if((evt.touches && evt.touches.length > 1)) {
            return;
        }
    
        this.addAllListeners()
        this.initialTouchPos = this.getGesturePointFromEvent(evt);
    }

    // Handle end gestures
    handleGestureEnd(evt) {
        evt.preventDefault();       
        if ((evt.touches && evt.touches.length > 0)) {
            return;
        }
    
        this.removeAllListeners()
        this.updateSwipeRestPosition(evt);
    
        this.initialTouchPos = null;
    }

    getGesturePointFromEvent = function (evt) {
        var point = {};
    
        if (evt.targetTouches) {
          // Prefer Touch Events
          point.x = evt.targetTouches[0].clientX;
          point.y = evt.targetTouches[0].clientY;
        } else {
          // Either Mouse event or Pointer Event
          point.x = evt.clientX;
          point.y = evt.clientY;
        }
    
        return point;
    }

    handleGestureMove(evt) {
        evt.preventDefault();
        if (!this.initialTouchPos) {
          return;
        }
      
        this.lastTouchPos = this.getGesturePointFromEvent(evt);
      
        this.onAnimFrame()
    }

    onAnimFrame() {
      
        let differenceInX = this.initialTouchPos.x - this.lastTouchPos.x;
        let newLeft = (0 - differenceInX)+'px';
        let leftStyle = newLeft;

        if(differenceInX > -100 && differenceInX < 100) {
            this.element.style.left = leftStyle;
        } else if (differenceInX <= -100) {
            this.element.style.left = '100%';
            setTimeout(function (){
                this.openModal(false)
            }.bind(this), 500)
            
            
        } else {
            this.element.style.left = '-100%';
            setTimeout(function (){
                this.openModal(true)
            }.bind(this), 500)
        }
    }

    resetIncidentSwipe() {
        this.element.style.left = '0';
    }

    updateSwipeRestPosition(evt) {
    
        this.addAllListeners()
        let differenceInX = this.initialTouchPos.x - this.lastTouchPos.x;
        if(differenceInX > -100 && differenceInX < 100) {
            this.element.style.left = '0';
        }
    
        this.initialTouchPos = this.getGesturePointFromEvent(evt);
    }

    closeModal() {
        const modal = this.element.querySelector('.modal');
        const modalBackdrop = this.element.querySelector('.modal-backdrop');
        
        modal.classList.remove('show');
        modalBackdrop.classList.remove('show');
        document.body.classList.remove('show-modal');
        this.addAllListeners()
    }

    openModal(isFinished) {
        this.turboFormHandlerTarget.setAttribute("src", this.turboFormHandlerTarget.dataset.src + (isFinished ? "/handled": "/not-handled"))

        this.removeAllListeners()
        const modalHeader = this.element.querySelector('.modal-header h1');
        modalHeader.textContent = isFinished ? "Afhandelen" : "Niet opgelost";
        const modal = this.element.querySelector('.modal');
        const modalBackdrop = this.element.querySelector('.modal-backdrop');
        
        modal.classList.add('show');
        modalBackdrop.classList.add('show');
        document.body.classList.add('show-modal');
        const exits = modal.querySelectorAll('.modal-exit');
        
        exits.forEach((exit) => {
            exit.addEventListener('click', (event) => {
                event.preventDefault();
                this.closeModal()
            });
        });
        setTimeout(function (){
            this.resetIncidentSwipe()
        }.bind(this), 1000)
    }
}

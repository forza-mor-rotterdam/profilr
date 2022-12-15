import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static targets = ["button", "turboFormHandler"]
    connect() {
        const frame = this.element.closest("turbo-frame")
        this.initialTouchPos = null
        this.rafPending = false
        this.finished = false // to prevent swiping when modal is open

        // Check if pointer events are supported.
        if (window.PointerEvent) {
            // Add Pointer Event Listener
            // this.element.addEventListener('click', this.openModal.bind(this), true);
            this.element.addEventListener('pointerdown', this.handleGestureStart.bind(this), true);
            this.element.addEventListener('pointermove', this.handleGestureMove.bind(this), true);
            this.element.addEventListener('pointerup', this.handleGestureEnd.bind(this), true);
            this.element.addEventListener('pointercancel', this.handleGestureEnd.bind(this), true);
        } else {
            // Add Touch Listener
            this.element.addEventListener('touchstart', this.handleGestureStart.bind(this), true);
            this.element.addEventListener('touchmove', this.handleGestureMove.bind(this), true);
            this.element.addEventListener('touchend', this.handleGestureEnd.bind(this), true);
            this.element.addEventListener('touchcancel', this.handleGestureEnd.bind(this), true);
            // Add Mouse Listener
            this.element.addEventListener('mousedown', this.handleGestureStart.bind(this), true);
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
            // this.closeModal()
            
        }
    }

    cancelHandleHandler(event) {
        this.closeModal()
    }

    // Handle the start of gestures
    handleGestureStart(evt) {
        evt.preventDefault();
        if((evt.touches && evt.touches.length > 1) || this.finished) {
            return;
        }
    
        // Add the move and end listeners
        if (window.PointerEvent) {
            this.element.setPointerCapture(evt.pointerId);
        } else {
            // Add Mouse Listeners
            this.element.addEventListener('mousemove', this.handleGestureMove.bind(this), true);
            this.element.addEventListener('mouseup', this.handleGestureEnd.bind(this), true);
        }
        this.initialTouchPos = this.getGesturePointFromEvent(evt);
    }

    // Handle end gestures
    handleGestureEnd(evt) {
        evt.preventDefault();       
    
        if ((evt.touches && evt.touches.length > 0) || this.finished) {
            return;
        }
        this.rafPending = false;
    
        // Remove Event Listeners
        if (window.PointerEvent) {
            this.element.releasePointerCapture(evt.pointerId);
        } else {
            // Remove Mouse Listeners
            this.element.removeEventListener('mousemove', this.handleGestureMove.bind(this), true);
            this.element.removeEventListener('mouseup', this.handleGestureEnd.bind(this), true);
        }
    
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
        if (!this.initialTouchPos 
            || this.finished) {
          return;
        }
      
        this.lastTouchPos = this.getGesturePointFromEvent(evt);
      
        if (this.rafPending) {
          return;
        }
      
        this.rafPending = true;
      
        this.onAnimFrame()
    }

    onAnimFrame() {
      
        if (!this.rafPending || this.finished) {
          return;
        }

        let differenceInX = this.initialTouchPos.x - this.lastTouchPos.x;
        let newLeft = (0 - differenceInX)+'px';
        let leftStyle = newLeft;

        if(differenceInX > -100 && differenceInX < 100) {
            this.element.style.left = leftStyle;
        } else if (differenceInX <= -100) {
            this.element.style.left = '100%';
            this.finished = true;
            setTimeout(function (){
                this.openModal(false)
            }.bind(this), 500)
            
            
        } else {
            this.element.style.left = '-100%';
            this.finished = true;
            setTimeout(function (){
                this.openModal(true)
            }.bind(this), 500)
        }
        this.rafPending = false;
    }

    resetIncidentSwipe() {
        this.element.style.left = '0';
    }

    enableIncidentSwipe() {
        this.finished = false;
    }

    updateSwipeRestPosition(evt) {
        let differenceInX = this.initialTouchPos.x - this.lastTouchPos.x;
        if(differenceInX > -100 && differenceInX < 100) {
            this.element.style.left = '0';
        }
    
        // Add the move and end listeners
        if (window.PointerEvent) {
            this.element.setPointerCapture(evt.pointerId);
        } else {
            // Add Mouse Listeners
            document.addEventListener('mousemove', this.handleGestureMove.bind(this), true);
            document.addEventListener('mouseup', this.handleGestureEnd.bind(this), true);
        }
    
        this.initialTouchPos = this.getGesturePointFromEvent(evt);
    }

    closeModal() {
        const modal = this.element.querySelector('.modal');
        const modalBackdrop = this.element.querySelector('.modal-backdrop');
        
        modal.classList.remove('show');
        modalBackdrop.classList.remove('show');
        document.body.classList.remove('show-modal');
        this.enableIncidentSwipe()
    }

    openModal(isFinished) {
        this.turboFormHandlerTarget.setAttribute("src", this.turboFormHandlerTarget.dataset.src + (isFinished ? "/handled": "/not-handled"))

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

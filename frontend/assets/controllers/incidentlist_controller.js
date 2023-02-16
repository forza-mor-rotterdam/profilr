import { Controller } from '@hotwired/stimulus';

let showSortingContainer = false;
let sortDirectionReversed = false;
export default class extends Controller {

    static targets = [ "sorting" ]

    
    initialize() {
        console.log('showSortingContainer', showSortingContainer)
    }

    connect(e) {
        
        if(this.hasSortingTarget && showSortingContainer === true ) {
            this.sortingTarget.classList.remove("hidden-vertical")
            this.sortingTarget.classList.add("show-vertical")
        }
    }

    onGroup(e) {
        console.log("onGroup", e.target.checked)
        const frame = document.getElementById('incidents_list');
        const url = `${frame.dataset.src}?grouped-by=${e.target.checked}`
        frame.setAttribute('src', url);
    }

    onToggleSortingContainer() {
        this.sortingTarget.classList.toggle("hidden-vertical")
        this.sortingTarget.classList.toggle("show-vertical")
        showSortingContainer = !showSortingContainer
        sortDirectionReversed = sortDirectionReversed === undefined ? false : true
    }

    onSort(e) {
        const frame = document.getElementById('incidents_list');
        const url = `${frame.dataset.src}?sort-by=${e.target.value}`
        frame.setAttribute('src', url);
    }
     
    makeRoute(e) {
        let routeUrl = "https://www.google.com/maps/dir"

        function handleCurrentLocation(pos) {
            const crd = pos.coords;
            routeUrl += `/${crd.latitude}+${crd.longitude}`
            getRoute()
        }

        function handleNoCurrentLocation(error) {
            switch(error.code) {
                case error.PERMISSION_DENIED:
                  console.log("User denied the request for Geolocation.")
                  break;
                case error.POSITION_UNAVAILABLE:
                  console.log("Location information is unavailable.")
                  break;
                case error.TIMEOUT:
                  console.log("The request to get user location timed out.")
                  break;
                case error.UNKNOWN_ERROR:
                  console.log("An unknown error occurred.")
                  break;
              }
            getRoute()
        }

        function getRoute() {
            e.params.incidents.map((incident)=> {
                let houseNumber = incident?.locatie?.adres?.huisnummer != undefined ? incident.locatie.adres.huisnummer : ""
                const address = `${incident?.locatie?.adres?.straatNaam} ${houseNumber} Rotterdam`
                routeUrl += `/${address}`
            })
            window.open(routeUrl, "_blank")
        }

        navigator.geolocation.getCurrentPosition(handleCurrentLocation, handleNoCurrentLocation);
    }
}

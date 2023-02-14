import { Controller } from '@hotwired/stimulus';

let showSortingContainer = false;
let sortDirectionReversed = false;
export default class extends Controller {

    static targets = [ "sorting" ]

    
    initialize() {

    }

    connect(e) {
        
        console.log('showSortingContainer 1', showSortingContainer)
        console.log('sortDirectionReversed 1', sortDirectionReversed)

        if(this.hasSortingTarget && showSortingContainer === true ) {
            this.sortingTarget.classList.remove("hidden-vertical")
            this.sortingTarget.classList.add("show-vertical")
        }
    }

    onToggleSortingContainer() {
        console.log('toggle')
        this.sortingTarget.classList.toggle("hidden-vertical")
        this.sortingTarget.classList.toggle("show-vertical")
        showSortingContainer = !showSortingContainer
        sortDirectionReversed = sortDirectionReversed === undefined ? false : true
        console.log('showSortingContainer 2', showSortingContainer)
        console.log('sortDirectionReversed 2', sortDirectionReversed)
    }

    onSort(e) {
        const frame = document.getElementById('incidents_list');
        
        sortDirectionReversed = !sortDirectionReversed
        const url = `${frame.dataset.src}?sort-by=${e.target.value}&reverse=${sortDirectionReversed}`
        console.log('url', url)
        frame.setAttribute('src', url);
    }
     
    makeRoute(e) {
        console.log('makeRoute', typeof(e.params.incidents))
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

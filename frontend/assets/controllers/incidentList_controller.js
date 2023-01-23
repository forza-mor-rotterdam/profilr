import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    
    connect() {
        
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

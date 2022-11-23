import { Controller } from '@hotwired/stimulus';

export default class extends Controller {
    static values = {
        incidentX: String,
        incidentY: String,
        areaList: String,
        currentDistrict: String
    }
    static targets = ['area', 'district', 'selectedImage', 'thumbList']
    
    initialize() {
        if(this.currentDistrictValue) {
            let currentArea = JSON.parse(this.areaListValue).find(area => area.buurten.some((district) => district.code === this.currentDistrictValue))
            this.areaTarget.textContent = currentArea.omschrijving
            this.districtTarget.textContent = currentArea.buurten.find((district) => district.code === this.currentDistrictValue).omschrijving
        } else {
            this.areaTarget.textContent = '-'
            this.districtTarget.textContent = '-'
        }

        if(this.hasThumbListTarget) {
            this.thumbListTarget.getElementsByTagName('li')[0].classList.add('selected')
        }
        
        const incidentCoordinates = this.rdToWgs84(Number(this.incidentXValue), Number(this.incidentYValue))
        const map = L.map('incidentMap', {
            zoomControl: false,
            maxZoom: 18,
            minZoom: 13,
            dragging: false,
            tap: false
        }).setView(incidentCoordinates, 16);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        const marker = L.marker(incidentCoordinates).addTo(map);

        const onTwoFingerDrag = (e) => {
            if (e.type === 'touchstart' && e.touches.length === 1) {
                e.currentTarget.classList.add('swiping')
            } else {
                e.currentTarget.classList.remove('swiping')
            }
        }
        document.getElementById('incidentMap').addEventListener('touchstart', onTwoFingerDrag);
        document.getElementById('incidentMap').addEventListener('touchend', onTwoFingerDrag);
    }

    selectImage(e) {
        const imgSrc = e.params.imageSource;
        this.selectedImageTarget.src = imgSrc;
        this.deselectThumbs(e.target.closest('ul'));
        e.target.closest('li').classList.add('selected')
    }

    deselectThumbs(list) {
        for (const item of list.querySelectorAll('li')) {
            item.classList.remove('selected');
        }
    }

    /**
     * Convert RD (Rijksdriehoek) coordinates to WGS84.
     * 
     */
    rdToWgs84(x, y=0) {
        const x0 = 155000;
        const y0 = 463000;
        const f0 = 52.15517440; // f => phi
        const l0 = 5.38720621;  // l => lambda
    
        const Kp = [0, 2, 0, 2, 0, 2, 1, 4, 2, 4, 1];
        const Kq = [1, 0, 2, 1, 3, 2, 0, 0, 3, 1, 1];
        const Kpq = [
        3235.65389,
        -32.58297,
        -0.2475,
        -0.84978,
        -0.0655,
        -0.01709,
        -0.00738,
        0.0053,
        -0.00039,
        0.00033,
        -0.00012,
        ];
    
        const Lp = [1, 1, 1, 3, 1, 3, 0, 3, 1, 0, 2, 5];
        const Lq = [0, 1, 2, 0, 3, 1, 1, 2, 4, 2, 0, 0];
        const Lpq = [
        5260.52916,
        105.94684,
        2.45656,
        -0.81885,
        0.05594,
        -0.05607,
        0.01199,
        -0.00256,
        0.00128,
        0.00022,
        -0.00022,
        0.00026,
        ];
    
        const Rp = [0, 1, 2, 0, 1, 3, 1, 0, 2];
        const Rq = [1, 1, 1, 3, 0, 1, 3, 2, 3];
        const Rpq = [190094.945, -11832.228, -114.221, -32.391, -0.705, -2.34, -0.608, -0.008, 0.148];
    
        const Sp = [1, 0, 2, 1, 3, 0, 2, 1, 0, 1];
        const Sq = [0, 2, 0, 2, 0, 1, 2, 1, 4, 4];
        const Spq = [309056.544, 3638.893, 73.077, -157.984, 59.788, 0.433, -6.439, -0.032, 0.092, -0.054];
    
        const dX = 1e-5 * (x - x0);
        const dY = 1e-5 * (y - y0);
    
        let lat = 0;
        let lon = 0;
  
        for (let i = 0; i < 10; i++) {
          lat = lat + Kpq[i] * dX ** Kp[i] * dY ** Kq[i];
        }
        lat = f0 + lat / 3600;
  
        for (let i = 0; i < 11; i++) {
          lon = lon + Lpq[i] * dX ** Lp[i] * dY ** Lq[i];
        }
        lon = l0 + lon / 3600;
  
        return [ lat, lon ];
    };
}

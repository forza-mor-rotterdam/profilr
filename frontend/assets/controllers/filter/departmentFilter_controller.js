import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        filters: String
    }

    connect() {
        const filterDepartmentList = JSON.parse(this.filtersValue).afdelingen ?? []
        const departmentCheckList = Array.from(document.getElementsByClassName('filter--department'))
        const countdepartmentDistricts = 0
        departmentCheckList.forEach(check => {
            if(filterDepartmentList.find(department => department[0] === check.value)) {
                check.checked = true
            }
        })
    }
}

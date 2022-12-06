import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        subjects: String,
        filters: String
    }

    connect() {
        const filterGroupList = JSON.parse(this.filtersValue).groepen ?? []
        const filterSubjectList = JSON.parse(this.filtersValue).onderwerpen ?? []
        const groupCheckList = Array.from(document.getElementsByClassName('filter--group'))

        console.log('filterGroupList', filterGroupList)
        console.log('filterSubjectList', filterSubjectList)
        
        groupCheckList.forEach(check => {
            console.log('check', check.value)
            if(filterGroupList.find(group => group[0] === check.value)) {
                console.log('group', group)
                check.checked = true
                //open nested districts
                check.closest('.container__check-group')
                    .getElementsByClassName('container__list--subject')[0]
                    .classList.remove('hidden')

                // check districts
                const subjectCheckList = Array.from(check.closest('.container__check-group')
                    .getElementsByClassName('filter--subject'))
                
                subjectCheckList.forEach(check => {
                    if(filterSubjectList.find(subject => subject[0] === check.value)) {
                        check.checked = true
                    }
                })
            }
        })
        console.log('connect Subjects', groupCheckList)
    }
    
    toggleGroup(e) {
        console.log('klik')
        const subjects = e.target.closest('li').getElementsByClassName('container__list--subject')[0]
        if(e.target.checked) {
            subjects.classList.remove('hidden')
        } else {
            const list = [].slice.call(subjects.getElementsByTagName('input'))
            list.forEach(input => {
                input.checked = false
            });
            subjects.classList.add('hidden')
        }
    }

    selectAreaFromDistrict(e) {
        const area = e.target.closest('.container__check-area').getElementsByTagName('input')[0]
        area.checked = true;
    }
}

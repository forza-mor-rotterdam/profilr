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

        groupCheckList.forEach(check => {
            if(filterGroupList.find(group => group[0] === check.value)) {
                // console.log('group', group)
                check.checked = true
                check.closest('.container__check-group')
                    .getElementsByClassName('container__list--subjects')[0]
                    .classList.remove('hidden')

                const subjectCheckList = Array.from(check.closest('.container__check-group')
                    .getElementsByClassName('filter--subject'))
                
                subjectCheckList.forEach(check => {
                    if(filterSubjectList.find(subject => subject[0] === check.value)) {
                        check.checked = true
                    }
                })
            }
        })
    }
    
    toggleGroup(e) {
        const subjects = e.target.closest('li').getElementsByClassName('container__list--subjects')[0]
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

    selectGroupFromSubject(e) {
        const group = e.target.closest('.container__check-group').getElementsByTagName('input')[0]
        group.checked = true;
    }
}

// showing the other complaint text field only when other complaint is selected.

 document.getElementById('id_complaint_type').onchange = function () {
    if(this.value == 'Other') {
        document.getElementById('id_complaint_type').setAttribute("disabled", "disabled")
        document.getElementById('id_other_complaint_type').removeAttribute("disabled")
    } else {
        document.getElementById('id_complaint_type').removeAttribute("disabled")
        document.getElementById('id_other_complaint_type').setAttribute("disabled", "disabled")
    }

}



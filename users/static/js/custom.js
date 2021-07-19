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




/* disabling and enabling the visitor id field based on visitor status.
document.getElementById('id_visiting_status').onchange = function() {
    if(this.value == 'Yes') {
        document.getElementById('id_visitor_id').disabled = false
    } else {
        document.getElementById('id_visitor_id').disabled = true
    }

}

*/



function checkOption(obj) {
    var input = document.getElementById("id_visitor_id");
    input.disabled = obj.value == "No" || obj.value == "Is the visitor a UG student?";
}



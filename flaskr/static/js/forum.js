function show_form(caller, name){
    var caller_btn = document.getElementById(caller);
    caller_btn.style.display = "none";

    var form = document.getElementById(name);
    form.style.display = "block";
}
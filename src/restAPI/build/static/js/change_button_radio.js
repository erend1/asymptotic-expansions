function change_button_radio(radio,button_id) {
  var btn = document.getElementById(button_id);
  if (radio.checked == true) {
    btn.disabled = "";
  } else {
    btn.disabled = "disabled";
  }
}
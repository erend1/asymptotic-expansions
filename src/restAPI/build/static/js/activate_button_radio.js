function ActivateButtonFromRadio(radio_id,button_id) {
  const radio = document.getElementById(radio_id);
  const btn = document.getElementById(button_id);
  if (radio.checked === true) {
    btn.setAttribute("aria-disabled", "true");
  } else {
    btn.setAttribute("aria-disabled", "true");
  }
}
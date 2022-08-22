var DateTime = luxon.DateTime;

for (const el of document.querySelectorAll("[data-date-fmt]")) {
  let date = null;
  if ("date" in el.dataset)
    date = DateTime.fromISO(el.dataset.date.replace(" ", "T"));
  else
    date = DateTime.now();
  el.innerHTML = date.toFormat(el.dataset.dateFmt);
}

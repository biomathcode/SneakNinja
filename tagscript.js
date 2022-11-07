// this will be the Js script that the users will add on there website.
// it will make a call on the main_app rest api to track user data.
// Collect data like country, time, id, session, device information.
// Other features like cursor heatmanp can be added afterwards.

if (document.readyState !== "loading") {
  sneakNinja();
} else {
  document.addEventListener("DOMContentLoaded", function () {
    sneakNinja();
  });
}

function sneakNinja() {
  var l = document.querySelector('script[data-name="sneakninja"]');

  var websiteId = l.dataset["websiteId"];

  var time = new Date().toISOString();

  var data = {
    websiteId,
    pageHref: "/",
    countryId: "INR",
    ssTime: time,
  };

  var jsondata = JSON.stringify(data);
  fetch("http://127.0.0.1:5000/api/v1", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: jsondata,
  }).then(() => console.log("SneakNinja was here"));
}

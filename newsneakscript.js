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

async function sneakNinja() {
  var l = document.querySelector('script[data-name="sneakninja"]');

  var websiteId = l.dataset["websiteId"];

  var time = new Date().toISOString();

  var data = {
    websiteId: websiteId || "1125899906842632",
    pageHref: "/",
    countryId: "INR",
    ssTime: time,
  };

  var jsondata = JSON.stringify(data);
  var resonse = await fetch("http://127.0.0.1:5000/api/v1", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: jsondata,
  });
  var jsonData = await resonse.json();
  console.log(jsonData);
}

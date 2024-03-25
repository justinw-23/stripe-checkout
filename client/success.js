var urlParams = new URLSearchParams(window.location.search);
var sessionId = urlParams.get('session_id');
console.log(sessionId);

if (sessionId) {
  fetch('/checkout-session?sessionId=' + sessionId)
    .then(function (result) {
      return result.json();
    })
    .then(function (session) {
      var filteredSession = {
        id: session.id,
        amount_subtotal: session.amount_subtotal,
        customer_details: session.customer_details,
        amount_total: session.amount_total,
        currency: session.currency,
        payment_status: session.payment_status
      };

      // Convert the filtered object to a JSON string
      var sessionJSON = JSON.stringify(filteredSession, null, 2);
      document.querySelector('pre').textContent = sessionJSON;
    })
    .catch(function (err) {
      console.log('Error when fetching Checkout session', err);
    });
}

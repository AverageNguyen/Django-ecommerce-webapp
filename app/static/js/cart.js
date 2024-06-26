var updateBTns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBTns.length; i++) {
  updateBTns[i].addEventListener("click", function () {
      var productId = this.getAttribute("data-product");
      var action = this.getAttribute("data-action");
    console.log("productId", productId, "action", action);
    console.log("user: ", user);
    if (user === "AnonymousUser") {
      console.log("chua dang nhap");
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function updateUserOrder(productId, action) {
  console.log("success");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ 'productId':productId, 'action': action }),
  })
    .then((response) => {
      if (!response.ok) {
          throw 'Error';
      }
      return response.json();
    })
    .then((data) => {
      console.log("data", data)
      location.reload()
    })
}

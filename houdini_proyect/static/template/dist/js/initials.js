function initial(user) {
  var name = user;
  var initials = name.charAt(0);
  console.log(initials);
  document.getElementById("name").innerHTML = initials;
}

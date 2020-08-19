function avatar(user, emailUser) {
  var name = "";
  var email = "";
  if (user.length > 22) {
    for (var i in user) {
      name += user.charAt(i);
      if (i == 18) {
        break;
      }
    }
    name += "...";
    document.getElementById("nombreAvatar").innerHTML = name;
  }
  if (emailUser.length > 22) {
    for (var i in emailUser) {
      email += emailUser.charAt(i);
      if (i == 8) {
        break;
      }
    }
    email += "...@gmail.com";
    document.getElementById("emailAvatar").innerHTML = email;
  }
}

function grant_revoke(id,privilege){
  var access=!privilege;
  var token="Token ";
  var token1=localStorage.getItem('auth');
  var authorization=token.concat(token1);
  fetch('http://127.0.0.1:8000/privilegeAuth/', {
    method: "PATCH",
    body: JSON.stringify({
      uid: id,
      adminPrivilege: access,
    }),
    headers: {
      "Authorization": authorization,
      "Content-type": "application/json; charset=UTF-8",
    },
  })
    .then(function (response) {
      console.log(response);
      if (!response.ok) {
        alert(response.statusText);
        return "notok";
      }
      return "ok";
    })
    .then(function (responseData) {
      if (responseData === "notok") {
        console.log("Bad response from server.");
      } else window.location.reload();
    });
}





function loop(data,str){
    var i;
    for (i = 0; i < data.length; i++) { 
      if(data[i]['name']===""){ continue;}
      if(data[i]['adminPrivilege']==false){
            $(str).append(
                  `
                  <li class="list-group-item list-group-item-info">${data[i]['name']}
                    <a type="button" class="btn btn-secondary" style="float: right;margin-left: 2px;color:white;" disabled>Revoke</a>
                    <a type="button" class="btn btn-success" style="float: right;color:white;" onclick='grant_revoke( ${data[i]['uid']},${data[i]['adminPrivilege']})'>Grant</a>
                  </li>
                  
                  `
                  );
        }else{
          $(str).append(
            `
            <li class="list-group-item list-group-item-info">${data[i]['name']}
              <a type="button" class="btn btn-success" style="float: right;color:white;margin-left: 2px;" onclick='grant_revoke( ${data[i]['uid']},${data[i]['adminPrivilege']})'>Revoke</a>
              <a type="button" class="btn btn-secondary" style="float: right;margin-left: 2px;color:white;" disabled>Grant</a>
            </li>
            
            `
            );

        }
    }
}


function logout(){
    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/logout/",
      success: function (data) {
        localStorage.removeItem('name');
        localStorage.removeItem('adminPrivilege');
        localStorage.removeItem('auth','');
        window.location.href="login.html";
   
      },
      error: function (response) {
        alert(response["statusText"]);
      },
    });
  }



  function loadUsers() {
    var token="Token ";
    var token1=localStorage.getItem('auth');
    var authorization=token.concat(token1);
    $.ajax({
      type: "GET",
      url: "http://127.0.0.1:8000/allUsers/",
      headers: {"Authorization": authorization},
      success: function (data) {
        console.log(data);
        loop(data,"#allusers");
        
   
      },
      error: function (response) {
        alert(response["statusText"]);
      },
    });

  }
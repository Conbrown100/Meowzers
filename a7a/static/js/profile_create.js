
function checkFields(){
  console.log( $('#usernameInput' ) );
}


$(function() {
    $(':submit').click(function() {
        alert("1");
        checkFields();
    });
});


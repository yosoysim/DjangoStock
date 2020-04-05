
 function calIndicator()   {

    /*lert('aa') ;

  if (!$('#txn_date').val()) {
    alert("거래일을 입력해 주세요.");
    return;

  $('#indicator_form').submit(); */
  //#$(location).attr('href', '/price/indicator_cal');

  $("#indicator_form").attr("action", "/price/indicator_cal"); /* elegabt url 사용하면 안 됨 */
  $("#indicator_form").submit();



}


function editIndicator() {

  /*method="POST*/
  /*$(location).attr('href', '/price/indicator_edit'); */ /* indicator_edit?mode=2 */
  /*$('#indicator_form').action = "{% url 'indicatorEdit' %}" ;*/
  $("#indicator_form").attr("action", "/price/indicator_edit"); /* elegabt url 사용하면 안 됨 */
  $("#indicator_form").submit();


}


function allRecalIndicator() {

  $("#indicator_form").attr("action", "/price/indicator_all_recal"); /* elegabt url 사용하면 안 됨 */
  $("#indicator_form").submit();


}
function cancelMemberRegisteraaa() {
  var result = confirm("회원가입을 취소하시겠습니까?");

  if (result)
  {
    $(location).attr('href', '/boardapp/login');
  }
}

function idCheckaaa() {
  if (!$('#username').val())
  {
    alert("ID를 입력해 주시기 바랍니다.");
    return;
  }

  $.ajax({
    type: "POST",
    url: "/boardapp/user_register_idcheck/",
    data: {
      'username': $('#username').val(),
      'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
    },
    success: idCheckResult,
    dataType: 'html'
  });  
}


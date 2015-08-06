// $( document ).ready(function() {
    alert( "ready!" );


  $(function(){
      $('#clickme').click(function(){
          $('#uploadme').click();
      });
  });

  function readURL(input) {
          if (input.files && input.files[0]) {
              var reader = new FileReader();

              reader.onload = function (e) {
                  $('#profileimage').attr('src', e.target.result);
              }

              reader.readAsDataURL(input.files[0]);
          }
      }

      $("#imgInp").change(function(){
          readURL(this);
      });

});

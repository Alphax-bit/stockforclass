$(document).ready(function(){

   $('.table').paging({limit:6});
   $(".datetimeinput").datepicker({changeYear: true, changeMonth: true, dateFormat: 'yyyy-mm-dd hh:mm'});
});
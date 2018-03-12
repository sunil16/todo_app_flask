
  $(document).ready(function(){

    
      $( function() {
        $( "#datepicker" ).datepicker();
      } );

      $( function() {
        $(".datepicker1").datepicker();
      });



      $(".taskli").click(function() {
         $(this).children(".CreateSubTask").css("visibility","visible");
         $(".datepicker1").datepicker();

      });


      $('#myInput').keyup(function(){

          var that = this, $allListElements = $('ul > li');

          var $matchingListElements = $allListElements.filter(function(i, li){
              var listItemText = $(li).text().toUpperCase(), searchText = that.value.toUpperCase();
              return ~listItemText.indexOf(searchText);
          });

          $allListElements.hide();
          $matchingListElements.show();

      });


      $("#dropdown").change(function(v){
      val = v.target.value;
      if (val ==  'Today') {
        $("#week").hide();
        $("#nextweek").hide();
        $("#overduedate").hide();
        $("#today").show();
      } else if (val == 'Week') {
        $("#today").hide();
        $("#nextweek").hide();
        $("#overduedate").hide();
        $("#week").show();
      } else if (val == 'Next Week') {
        $("#today").hide();
        $("#week").hide();
        $("#overduedate").hide();
        $("#nextweek").show();
      } else if (val == 'Over Due Date') {
        $("#today").hide();
        $("#week").hide();
        $("#nextweek").hide();
        $("#overduedate").show();
      } else {
        $("#today").show();
      }
  });

  });

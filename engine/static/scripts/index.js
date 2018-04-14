
var host = "http://localhost:5000"
// Get the header
var header, sticky;
var requesting = false;


var data = {}
var date_options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
$(document).ready(function () {

    // Get the header
     header =$("#myHeader");
       // Get the offset position of the navbar
     sticky = header.offset().top
 
     
     $('#search-text').keypress(function(e){
      if(e.keyCode==13){
          if(requesting)
              return;
          requesting = true;
          search();
      }
      
    });
    
});


$(document).on({
    
    ajaxStart: function() { $("body").addClass("loading");    },
    ajaxStop: function() { $("body").removeClass("loading"); requesting = false;}    ,
    ajaxError: function() { $("body").removeClass("loading");  requesting = false;},
    ajaxSuccess: function() { $("body").removeClass("loading"); requesting = false; }     
});

var search = function(){
     var text = $('#search-text').val();
    
     console.log("Query: "+ text );
     
     var content = $("#content");

     content.empty();
         
     data = {};
     
     //content.append("<div style='text-align:center' class='loader'></div>");
     $.ajax({
          url: host+"/api/query",
          type: "get", //send it through get method
          data: { 
            q: text
         
          },
          timeout: 5000, // sets timeout to 5 seconds
          success: function(response) {
           console.log(response)
           cheader = $("<div class='row'> </div>")
           body = $("<div class='row'> </div>")
           
           total = response.total 
           
           if(total == 0){
               var element = $('<h1></h1>')
               element.html("There no results")
               cheader.append(element)
      
               
           }else{
               
              for (var index = 0; index < response.records.length; ++index) {
              
                    record = response.records[index];
                    
                    //console.log(record)
                    class_code = record.class_code
                    
                    var container = $("<div class='row'></div>")
                    
                    var title_element = $('<h1></h1>')
                    
                    if(class_code == 1){
                    
                        title_element.addClass("link-very-positive")
                    }else if(class_code == 4){
                    
                        title_element.addClass("link-very-negative")
                    }else if (class_code==2){
                            title_element.addClass("link-positive")
                    }else {
                            title_element.addClass("link-negative")
                    }
                    
           
                    
                    title_element.html(record.title)
                    title_element.on('click',{index:index},f)
                    
                    container.append(title_element)
                    
                    // DATE
                    date = new Date(record.date*1000)
                    date_element = $('<h3>'+date.toLocaleString("en-US",date_options)+'</h3>')
                    container.append(date_element)
                    
                    body.append(container);
                    data[index] = record;
              }
              cheader.html("Found "+ total +" results")
                           
           }
           
           body.removeClass("loading")
           content.append(cheader);
           
           content.append(body);
          },
          error: function(xhr) {
            //Do Something to handle error
            console.log(xhr)
          }
        });
     
     $("#results").add("<h1>Test</h1>")
}

function f(event){
    index = event.data.index
    record = data[index];
    
    var modal = $("#myModal")
    
    console.log(index)
    modal.find('.modal-title').text(record.title);
    
    content =  modal.find('.modal-body');
    
    content.empty();
    
    
    
    content.html(record.content)
    
    modal.modal('show');
}

// When the user scrolls the page, execute myFunction
window.onscroll = function() {updateScroll()};

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
function updateScroll() {

  if (window.pageYOffset >= sticky) {
    header.addClass("sticky");
  } else {
    header.removeClass("sticky");
  }
} 

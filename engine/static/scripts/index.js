
var host = "http://localhost:5000"
// Get the header
var header, sticky;
var requesting = false;


var data = {}
var date_options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' ,time:'numeric', timeZone: 'UTC' };
var days_before = -1;
var sent = -1;

$(document).ready(function () {

    // Get the header
     header =$("#myHeader");
       // Get the offset position of the navbar
     sticky = header.offset().top

     
     $('#search-text').keypress(function(e){
      if(e.keyCode==13){
          if(requesting)
              return;
         
          var text = $('#search-text').val();
 
          if( 0 === text.length)
             return;
        
          requesting = true;
          search(text,"/api/query");
      }
      
    });
    
  
    requesting = true;
    topics();
    
        var text = $('#search-text').val();
 
      if( 0 != text.length){
         
          requesting = true;
          search(text,"/api/query");
      }
 
});


$(document).on({
    
    ajaxStart: function() { $("body").addClass("loading");    },
    ajaxStop: function() { $("body").removeClass("loading"); requesting = false;}    ,
    ajaxError: function() { $("body").removeClass("loading");  requesting = false;},
    ajaxSuccess: function() { $("body").removeClass("loading"); requesting = false; }     
});


var topics = function(){


     
     var content = $("#topics");

     content.empty();
         
     data = {};
     
     $.ajax({
          url: host+"/api/hotTopics",
          type: "get", //send it through get method
          timeout: 8000, // sets timeout to 5 seconds
          data: { 
            d: days_before,
            s: sent
          },
          success: function(response) {
      
           body = $("<div class='row' style='text-align:right'></div>")
                          
  
           total = response.total 
           
           if(total == 0){
               var element = $('<h1></h1>')
               element.html("There no topics")
               body.append(element)
      
               
           }else{
              
              var title_element = $('<h1>Hot Topics</h1>')
              body.append(title_element);                      
              for (var index = 0; index < response.length; ++index) {
              
                    record = response[index];
                    
                    //console.log(record)
                    name = record.name
                    count = record.count
     
                    
                    var title_element = $('<h3></h3>')
                      
                    title_element.html(name+'<span class="badge badge-dark">'+count+'</span>')
                    title_element.on('click',{topic:name},searchTopic)
                    title_element.addClass("link-topic")
             
                    
       
                    body.append(title_element);

              }
             
                           
           }
           
           body.removeClass("loading")

           
           content.append(body);
          },
          error: function(xhr) {
            //Do Something to handle error
            console.log(xhr)
          }
        });
     
    
}

var search = function(text,query){

     var content = $("#news");

     content.empty();
         
     data = {};
     
     $.ajax({
          url: host+query,
          type: "get", //send it through get method
          data: { 
            q: text,
            d: days_before,
            s: sent
         
          },
          timeout: 8000, // sets timeout to 5 seconds
          success: function(response) {
         
           cheader = $("<div class='row'> </div>")
           body = $("<div class='row'> </div>")
           
           total = response.total 
           retrieved= response.retrieved 
           
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
                    title_element.on('click',{index:index},showModal)
                    
                    container.append(title_element)
                    
                    // DATE
                    date = new Date(record.date*1000)
               
                    date_element = $('<h3>'+date.toLocaleString("en-US",date_options)+" "+ date.toLocaleTimeString("en-US",{ timeZone: 'UTC'})+'</h3>')
                    container.append(date_element)
                    
                    body.append(container);
                    data[index] = record;
              }
              cheader.html("Found "+ total +" results. Retrieved top "+retrieved)
                           
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
}

function searchTopic(event){
   topic = event.data.topic
   if(requesting)
      return;

   requesting = true;
   search(topic,"/api/queryTopic");
}
function showModal(event){
    index = event.data.index
    record = data[index];
    
    var modal = $("#myModal")
    
    console.log(index)
    modal.find('.modal-title').text(record.title);
    
    content =  modal.find('.modal-body');
    
    content.empty();
    
    
    
  
    content.append('<p>'+record.content+'</p>')
    content.append('<br>')
    content.append('<a href="'+record.link+'" target="_blank">'+record.link+'</a>')
     // link = record.link
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


function update(d){
  id = 'd'+d;

  $(".days").each(function( index ) {
      $(this).removeClass('big') ;
    });
  var el = $("#"+id)
  el.addClass('big')
  
  days_before = d;
  if(requesting)
      return;
  requesting = true;   
  topics();
  

   var text = $('#search-text').val();
 
   if( 0 === text.length)
     return;

   requesting = true;
   search(text,"/api/query");
}

function updateS(d){
  id = 's'+d;

  $(".sent").each(function( index ) {
      $(this).removeClass('big') ;
    });
  var el = $("#"+id)
  el.addClass('big')
  
  sent = d;
  if(requesting)
      return;
  requesting = true;   
  topics();
  

   var text = $('#search-text').val();
 
   if( 0 === text.length)
     return;

   requesting = true;
   search(text,"/api/query");
}
'use strict'
// var host ="http://localhost:8000/";
var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/'

window.onload = function(){
  var div = $(".target")
  // console.log(div[0].innerHTML);
  $.get( host + "upcoming_courses", function( response ) {
    // alert( "Load was performed." );
    const data = JSON.parse(response)
    console.log(data);
    let html = ""

    let broken_down = [];
    let in_fours = [];
  
    for (let i = 0; i < data.length; i++) {
      in_fours.push(data[i]);
      if ((i+1)%4 == 0 || i+1 == data.length){
            broken_down.push(in_fours);
            in_fours = [];
        }
      
    };
    console.log(broken_down);

    for (let i = 0; i < broken_down.length; i++) {
  
        console.log((i+1)% 4);
        let status = (i == 0 ? "active" : "");
        // i = (data.length - i < 4 ? i : data.length);

        html += `<div class="item ${status}">
  
        ${create_div(broken_down[i], 0)}

        ${create_div(broken_down[i], 1)}
    
        ${create_div(broken_down[i], 2)}
  
        ${create_div(broken_down[i], 3)}
  
      </div>`
   
      }
      div[0].innerHTML = html;
    


  });
  
}

function create_div(_list, index){
  if(_list.length > index){
    
    console.log(_list[index].fields.title, index);
    let div = `
    <div class="col-xs-12 col-md-6">
              <div class="recta_box">
              <i class="fa fa-angle-right arrow-right"></i>
              <div class="imgpart"><img src='${host}media/${_list[index].fields.image}' alt="img01" /></div>
              <div class="contpart">
              <h4>${_list[index].fields.title} </h4>
              <div class="date"><i class="fa fa-calendar"></i> &nbsp;&nbsp;Starts  ${convert_date(_list[index].fields.date)}</div>
              <div class="time"><i class="fa fa-clock-o"></i> &nbsp;&nbsp;${_list[index].fields.time}</div>
              <a href="/detailed_course_view/${_list[index].pk}">Apply Now</a>
              </div>
              </div>
              </div>
              `

      return div
  }
  else{
    return `
            <div class="col-xs-12 col-md-6">
            <div class="recta_box"  id = "trans">
            <p class ="space">&nbsp;</p>
            </div>
          </div>
              `
  }

}


function convert_date(_date){
  let fixed_date = new Date(_date).toString()

  // ACTUAL DATE INCLUDES DAY NAME BELOW LINE SLICES THE EXCESS DATA AND THEN ADDS . AND COMMA TO MAKE LOOK STANDARD Jan., 06 2019
  return fixed_date.slice(4, 16).replace(/\s/,'., ');
}
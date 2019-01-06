'use strict'
// var host ="http://localhost:8000/";
var host = window.location.hostname == 'localhost'
    ? 'http://localhost:8000/'
    : 'http://' + window.location.hostname + '/'

window.onload = function(){

  var men = $('.button')
  // console.log(data)
  
  $('form').on('submit', e => {
      e.preventDefault()
      let data = $('.application_form') // add lives_in select value to post data
      console.log(data)
      swal({
        title: "Are you sure?",
        text: `Hi ${data[0][2].value}, Do you confirm that the data supplied is accurate ?.`,
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          
          // POST DATA IF USER CLICKS YES
          post();
        } else {
          swal(`Post Cancelled !!!`);
        }
      });
  
  
  
  // FUNCTION TO POST NOW HANDLED BY SWAL FROM SWEET ALERT
      const post = ()=>{
        let csrftoken = $('[name="csrfmiddlewaretoken"]')[0].value
        let course_id = $('#course_id')[0].innerHTML
        
        let form_data = $('#application_form').serialize() // add lives_in select value to post data
        console.log(form_data);
        function csrfSafeMethod (method) {
              // these HTTP methods do not require CSRF protection
          return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
        }
      
        $.ajaxSetup({
          beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader('X-CSRFToken', csrftoken)
            }
          }
        })
      
        $.post(host + 'apply/' + course_id + '/' , form_data)
              .then(resp => {
                console.log(resp)
                console.log(JSON.parse(resp))
                resp = JSON.parse(resp)
                if (resp.response == 'success') {
                  swal({
                    title: "Successful",
                    text : `Your application has been submitted.!!!`,
                    icon: "success",
                  });
                } else if (resp.response == 'fail') {
                  swal({
                    title: "Unknown Error",
                    text: `Sorry an unknown error occurred`,
                    icon: "error",
                  });
                }
              })
              .catch(() => {
                swal( {
                  title: "Fatal Error",
                  text: `Could be network, please check your internet connection.!!`,
                  icon: "error",
                });
              }) // post data
  
  
      }
      
      
    })
}

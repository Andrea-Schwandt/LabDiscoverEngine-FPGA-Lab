fpga_prog = 0;
update_image = 0;
timeout1_value = 200;
timeout2_value = 400;
active_timeout1 = 0;
active_timeout2 = 0;
active_timeout3 = 0;

$("#current_response").text("___.__ mA");
$("#fpga_response").text("You are working on FPGA: CX2");


img_upload_path = "http://10.30.200.157/labfiles/images/upload_image.jpg";
img_out_path = VIDEO_URL;
img_icon_path = "http://10.30.200.157/labfiles/Logos/EduPow_CX.jpg";
error_img_path = "http://10.30.200.157/labfiles/output_images/C_X/image_error_CX.jpg";

$("#core_voltage").text("1.0 V");

function clean() {
    $("#panel").hide();
    // No more time
    $("#timer").text("Time is over!");
    $("#back-url").css("display", "block");
    running = false;
    currentTime = 0;
    clearInterval(STATUS_INTERVAL);
    clearInterval(TIMER_INTERVAL);
}

function updateTime () {
    currentTime = currentTime - 1;
    if (currentTime > 0) {
        // Still time
        if (currentTime > 1)
            $("#timer").text(currentTime + " seconds");
        else
            $("#timer").text(currentTime + " second");
        if (currentTime < 30){
            $("#timer").css("color", "red");
        } 
        else if (currentTime < 60){
            $("#timer").css("color", "orange");
        } 
        else {
            $("#timer").css("color", "black");
        }
    } else {
        clean();
    }
}

updateTime();

function sendProgram(code) {
    $.post(FPGA_URL, {
        csrf: CSRF,
        code: code
    }).done(parseStatus);
}

new_image = new Image(440);
new_image.src = "http://10.30.200.157/labfiles/output_images/output.jpg"; 

image_no = 0;
input_image_array = ["http://10.30.200.157/labfiles/images/street_0.jpg",
                    "http://10.30.200.157/labfiles/images/street_1.jpg",
                    "http://10.30.200.157/labfiles/images/street_2.jpg",
                    "http://10.30.200.157/labfiles/images/street_3.jpg",
                    "http://10.30.200.157/labfiles/images/street_4.jpg",
                    "http://10.30.200.157/labfiles/images/street_5.jpg",
                    "http://10.30.200.157/labfiles/images/street_6.jpg",
                    "http://10.30.200.157/labfiles/images/street_7.jpg",
                    "http://10.30.200.157/labfiles/images/Testbild_FH.jpg",
                    "http://10.30.200.157/labfiles/images/upload_image.jpg",  //liegt auf dem experiment server
                    "http://10.30.200.157/labfiles/images/a_stripes0.jpg",
                    "http://10.30.200.157/labfiles/images/b_stripes1.jpg",
                    "http://10.30.200.157/labfiles/images/c_stripes2.jpg"]
input_image_alt_array = ["Motorway in Germany",
                        "Motorway in Germany",
                        "Road in Germany",
                        "Road in Germany",
                        "Road on Canary Islands, Spain",
                        "Road in Andes mountains, Argentina",
                        "Road in Germany, difficult for lane detection because of poor road markings",
                        "Bridge in Denmark, difficult for lane detection because of poor visibility due to rain",
                        "Test card with lower switching activity that should result in lower dynamic power consumption",
                        "Here you can upload/see your own JPEG image, recommended resolution is 1280x720 pixel",
                        "stripes0",
                        "stripes1",
                        "stripes2"]
new_input_image = new Image(440);
new_input_image.src = "http://10.30.200.157/labfiles/images/Testbild_FH.jpg"; 

// Get the modal
var modal = document.getElementById('myModal');

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img_in = document.getElementById('input_img');
var img_out = document.getElementById('output_img');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
img_in.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
}

img_out.onclick = function(){
    modal.style.display = "block";
    modalImg.src = this.src;
    //captionText.innerHTML = this.alt;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
    modal.style.display = "none";
}

function program_notify() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = "http://10.30.200.157/labfiles/output_images/image_programming_FPGA.jpg"+rfsh;
    document.images.output_img.src = new_image;
  }

  function update_notify() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = "http://10.30.200.157/labfiles/output_images/image_update.jpg"+rfsh;
    document.images.output_img.src = new_image;
    console.log("notify", active_timeout1);
  }

  function upload_notify() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_input_image = "http://10.30.200.157/labfiles/images/image_uploading_image.jpg"+rfsh;
    document.images.input_img.src = new_input_image;
  }

  function upload_notify_output() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = "http://10.30.200.157/labfiles/output_images/image_uploading_image.jpg"+rfsh;
    document.images.output_img.src = new_image;
  }

  function update_img() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = img_out_path+rfsh;  //liegt auf dem experiment server
    document.images.output_img.src = new_image;
  }
  function update_icon() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = img_icon_path+rfsh;  
    document.images.board_img.src = new_image;
  }

  function update_input_image() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    if (image_no == 9){
      new_input_image = img_upload_path+rfsh;
    }
    else{
      new_input_image = input_image_array[image_no]+rfsh;
    }
    document.images.input_img.src = new_input_image;
    document.images.input_img.alt = input_image_alt_array[image_no];
  }

  function error_img() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = error_img_path+rfsh;
    document.images.output_img.src = new_image;
  }

  function no_input_image(){
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_image = "output_images/image_no_input.jpg"+rfsh;
    document.images.output_img.src = new_image;
  }

  function missing_img() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_input_image = "images/image_upload_error.jpg"+rfsh;
    document.images.input_img.src = new_input_image;
    if (fpga_prog){
      no_input_image();
    }
  }

  function wrong_format() {
    rfsh = new Date() ; rfsh = "?"+rfsh.getTime()
    new_input_image = "images/default/image_upload_jpeg_error.jpg"+rfsh;
    document.images.input_img.src = new_input_image;
    if (fpga_prog){
      no_input_image();
    }
  }

  function update_core_current() {
      $("#am_response").text("Measuring core current... ");
      $.post(MEASURE_URL, {
        csrf: CSRF
    })
    .done(function (response) {
         // The response message is a regular string
         $("#current_response").text(response);
         $("#am_response").text("ready");
      })
     .fail(function (error) {
         $("#am_response").text("There was an error: " + error);
     });
  }

  function check_file_size() {
      var img_file = document.getElementById(img_id).files[0];

      if ( img_file ){
          if ( img_file.type.match('image.*') ){
              $("#response").text("Your image file will be uploaded!!!!!");
              return 1;
          }
          else{
              $("#response").text("Sorry, wrong file format!!!!!");
              wrong_format();
              return 0;
          }
      }
      $("#response").text("Sorry, no image file!!!!! Please select a JPEG image prior pressing the <upload image> button");
      missing_img();
      return 0;
  }

  function check_fpga_file_size() {
      var fpga_file = document.getElementById(fpga_id).files[0];

      if ( fpga_file ){
          $("#bitfileResponse").text("Your bit file will be programmed!!!!!");
          return 1;
      }
      error_img()
      $("#bitfileResponse").text("Sorry, no bit file!!!!!");
      return 0;
  }

  function fpga_input_field(){
      var input=document.createElement('input');
      input.type="file";
      input.id="bitfile";
      input.accept=".sof";
      input.style="padding: 10px" 
      document.getElementById('fpga_file_div').appendChild(input);
  }

  function input_field(){
      var input=document.createElement('input');
      input.type="file";
      input.style="padding-bottom: 5px" 
      input.id="img_file0";
      input.accept=".jpg, .jpeg";
      document.getElementById('img_file_div').appendChild(input);
  }

  function sw0_on() {
      weblab.sendCommand("sw0_on")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw0_off() {
      weblab.sendCommand("sw0_off")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw1_on() {
      weblab.sendCommand("sw1_on")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw1_off() {
      weblab.sendCommand("sw1_off")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw2_on() {
      weblab.sendCommand("sw2_on")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw2_off() {
      weblab.sendCommand("sw2_off")
      .done(function(response) {
          if (fpga_prog){
              if (update_image){
                  update_output();
                  $("#input_img_response").text("Update image...");
              }
              update_core_current();
          }
      })
      .fail(function (error) {
          console.log("Error connecting Raspberry pi", error);
          $("#fileResponse").text("FAILED to connect to raspberry pi: " + error);
      });
  }

  function sw0() {
      var active = document.getElementById("myonoffswitch0").checked;
      if (active){
          sw0_on();
      }
      else {
          sw0_off();
      }
  }

  function sw1() {
      var active = document.getElementById("myonoffswitch1").checked;
      if (active){
          sw1_on();
      }
      else {
          sw1_off();
      }
  }

  function sw2() {
      var active = document.getElementById("myonoffswitch2").checked;
      if (active){
          sw2_on();
      }
      else {
          sw2_off();
      }
  }

  function disable_buttons(){
      console.log("button", active_timeout2);
      document.getElementById("image_first_button").disabled = true;
      document.getElementById("image_last_button").disabled = true;
      document.getElementById("image_next_button").disabled = true;
      document.getElementById("image_end_button").disabled = true;
      //document.getElementById("imgfile_button").disabled = true;
      //document.getElementById("bitfile_button").disabled = true;
      document.getElementById("bitfile1_button").disabled = true;
      document.getElementById("bitfile2_button").disabled = true;
      document.getElementById("bitfile3_button").disabled = true;
  }

  function disable_switches(){
      document.getElementById("myonoffswitch0").disabled = true;
      document.getElementById("myonoffswitch1").disabled = true;
      document.getElementById("myonoffswitch2").disabled = true;
  }

  function enable_buttons(){
      document.getElementById("image_first_button").disabled = false;
      document.getElementById("image_last_button").disabled = false;
      document.getElementById("image_next_button").disabled = false;
      document.getElementById("image_end_button").disabled = false;
      //document.getElementById("imgfile_button").disabled = false;
      //document.getElementById("bitfile_button").disabled = false;
      document.getElementById("bitfile1_button").disabled = false;
      document.getElementById("bitfile2_button").disabled = false;
      document.getElementById("bitfile3_button").disabled = false;
  }

  function enable_switches(){
      document.getElementById("myonoffswitch0").disabled = false;
      document.getElementById("myonoffswitch1").disabled = false;
      document.getElementById("myonoffswitch2").disabled = false;
  }

  function update_output(){
      console.log("Begin1", active_timeout1);
      console.log("Begin2", active_timeout2);
      if (active_timeout1 != 0){
          clearTimeout(active_timeout1);
          console.log("cleared1", active_timeout1);
          active_timeout1 = 0
      }
      if (active_timeout2 != 0){
          clearTimeout(active_timeout2);
          console.log("cleared2", active_timeout2);
          active_timeout2 = 0
      }
      if (active_timeout3 != 0){
          clearTimeout(active_timeout3);
          console.log("cleared3", active_timeout3);
          active_timeout3 = 0
      }
      active_timeout1 = setTimeout(function(){
          document.getElementById("output_img").style.opacity = "0.5";
          document.getElementById("ov_img").style.opacity = "1";
          timeout1_value = 600;
          active_timeout2 = setTimeout(function(){
              document.getElementById("output_img").style.opacity = "1";
              document.getElementById("ov_img").style.opacity = "0";
              $("#response").text("Please wait for image update... ");
              $("#am_response").text(" ... ");
              disable_buttons();
              disable_switches();
              active_timeout3 = setTimeout(function(){
                  if (update_image){
                      update_notify();
                  }
                  else
                  {
                      update_img();
                  }
                  enable_buttons();
                  enable_switches();
                  timeout1_value = 200;
              },600);
              console.log("timeout3", active_timeout3);
          },timeout2_value);
          console.log("timeout2", active_timeout2);
      },timeout1_value);
      console.log("timeout1", active_timeout1);
  }

fpga_input_field();
input_field();
document.getElementById("imgfile_button").disabled = true;
document.getElementById("bitfile_button").disabled = true;


$("#image_first_button").click( function() {
    image_no = 0;
        update_input_image();

        $.post(IMG_HOME, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
            if (fpga_prog){
                update_output();
                update_core_current();
            }
        });
});

$("#image_end_button").click( function() {
image_no = input_image_array.length - 4;
    update_input_image();

    $.post(IMG_END, {
        csrf: CSRF
    })
    .done(function (response) {
        $("#input_img_response").text("Update output image to get results");
    if (fpga_prog){
            update_output();
            update_core_current();
        }
    }); 
});

$("#image_last_button").click( function() {
    if (image_no > 0){
        image_no --;}
    else {
        image_no = input_image_array.length - 4;
    }
    update_input_image();

    if (image_no == 0) {
        $.post(IMG_LAST, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
        if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    }
    else if (image_no == (input_image_array.length - 4)) {
        $.post(IMG_LAST, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
        if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    }
    else {
        $.post(IMG_LAST, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
        if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    } 
});

$("#image_next_button").click( function() {
    if (image_no < (input_image_array.length - 4)){
        image_no ++;}
    else {
        image_no = 0;}
    update_input_image();

    if (image_no == 0) {
        $.post(IMG_NEXT, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
        if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    }
    else if (image_no == (input_image_array.length - 4)) {
        $.post(IMG_NEXT, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
        if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    }
    else {
        $.post(IMG_NEXT, {
            csrf: CSRF
        })
        .done(function (response) {
            $("#input_img_response").text("Update output image to get results");
            if (fpga_prog){
                update_output();
                update_core_current();
            }
        })
        .fail(function (error) {
            $("#input_img_response").text("There was an error: " + error);
        });
    } 
});

$("#bitfile_button").click( function() {
    $("#fileResponse").text("Programming...COMING SOON ");
    program_notify();
    $("#response").text(" ... ");
    $("#am_response").text(" ... ");

    fpga_id = document.getElementById("bitfile").id;
    var fpga_file = document.getElementById(fpga_id).files[0];

});

$("#bitfile1_button").click( function() {
    $("#fileResponse").text("Programming... ");
    program_notify();
    $("#response").text(" ... ");
    $("#am_response").text(" ... ");

    $.post(INVERT_PROG_URL, {
        csrf: CSRF
    })
    .done(function(response) {
        $("#fileResponse").text("Programming... " + response);
        fpga_prog = 1;
        update_output();
        update_core_current();
        setInterval(update_core_current,5000);
    })
    .fail(function (error) {
        console.log("File sent failed!", error);
        $("#fileResponse").text("FAILED: " + error);
    }); 
});

$("#bitfile2_button").click( function() {
    $("#fileResponse").text("Programming... ");
    program_notify();
    $("#response").text(" ... ");
    $("#am_response").text(" ... ");

    $.post(FILTER_PROG_URL, {
        csrf: CSRF
    })
    .done(function(response) {
        $("#fileResponse").text("Programming... " + response);
        fpga_prog = 1;
        update_output();
        update_core_current();
        setInterval(update_core_current,5000);
    })
    .fail(function (error) {
        console.log("File sent failed!", error);
        $("#fileResponse").text("FAILED: " + error);
    }); 
});

$("#bitfile3_button").click( function() {
    $("#fileResponse").text("Programming... ");
    program_notify();
    $("#response").text(" ... ");
    $("#am_response").text(" ... ");

    $.post(EDGE_PROG_URL, {
        csrf: CSRF
    })
    .done(function(response) {
        $("#fileResponse").text("Programming... " + response);
        fpga_prog = 1;
        update_output();
        update_core_current();
        setInterval(update_core_current,5000);
    })
    .fail(function (error) {
        console.log("File sent failed!", error);
        $("#fileResponse").text("FAILED: " + error);
    }); 
});

$("#imgfile_button").click( function() {

    img_id = document.getElementById("img_file0").id;
    upload_notify();
    if (fpga_prog){
        $("#am_response").text(" ... ");
        upload_notify_output();
    }
    if ( check_file_size() ) {
        $("#response").text("Please wait for image to upload... COMING SOON");
    }
    else {
        $("#response").text("Sorry, but: no image file -> no upload ;o) Please select a JPEG image prior pressing the <upload image> button");
        missing_img();
    }
});




function logout() {
    $.post(LOGOUT_URL, {
        csrf: CSRF
    }).done(function () {
        clean();
    });
}

var HIDE_MESSAGES_BOX = null;


var TIMER_INTERVAL = setInterval(updateTime, 1000);

$.get(STATUS_URL).done(parseStatus);


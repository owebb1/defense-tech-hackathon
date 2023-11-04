$(function() {
  var wakeInterval;
  var alarmTriggered = false;

  $("#boat").draggable({
    containment: "#ocean",
    drag: function(event, ui) {
      clearInterval(wakeInterval);
      createWake(ui.position);
      wakeInterval = setInterval(function() {
        checkBuoyCollision();
      }, 100); // Check every 100 milliseconds
    },
    stop: function(event, ui) {
      clearInterval(wakeInterval);
      checkBuoyCollision();
    }
  });
  var wakes = [];

function createWake(position) {
  var wake = $("<div class='wake'></div>");
  $("#ocean").append(wake);

  // You might need to adjust the offset for 'top' depending on the size of your boat image
  var wakeOffsetTop = 25; // Adjust this value as needed

  wake.css({
    "top": position.top + wakeOffsetTop + "px", // Positioned down from the boat
    "left": position.left - wake.width() + "px", // Starts from the left side of the boat
  }).animate({
    "width": "100px", // The wake expands
    "height": "50px", // The wake expands
    "top": position.top + wakeOffsetTop - (wake.height() / 2) + "px", // Adjust the vertical position during the animation
    "left": position.left - 100 + "px", // Move left as it expands
    "opacity": 0
  }, 3000, function() {
    // Remove the wake from the DOM and the wakes array
    var index = wakes.indexOf(this);
    if (index > -1) {
      wakes.splice(index, 1);
    }
    $(this).remove();
  });

  // Add the wake element and its initial position to the wakes array
  wakes.push({
    element: wake,
    position: position
  });
}


  // Then, in your collision checking, you can call this modified function:
  // setInterval(function() {
  //   wakes.forEach(function(wake) {
  //     checkBuoyCollision(wake.position, wake.element);
  //   });
  // }, 100); // Check for collisions every 100 milliseconds

function checkBuoyCollision() {
    wakes.forEach(function(wakeData) {
      var wakeBounds = wakeData.element[0].getBoundingClientRect();
      var buoyBounds = $(".buoy")[0].getBoundingClientRect();

      var isCollision = !(buoyBounds.left > wakeBounds.right ||
                          buoyBounds.right < wakeBounds.left ||
                          buoyBounds.top > wakeBounds.bottom ||
                          buoyBounds.bottom < wakeBounds.top);

      if (isCollision && !alarmTriggered) {
        alarmTriggered = true; // Set the flag to indicate the alarm is triggered
        wakeData.element.stop(); // Stop the wake expansion
        runSensorDataAndSoundAlarm();
      }
    });
  }

   function runSensorDataAndSoundAlarm() {
    $.ajax({
      url: '/detect',
      type: 'GET',
      success: function(data) {
        if (data.alarm_message) {
          $(".buoy").css('background-color', 'red');
        }
        alarmTriggered = false; // Reset the flag after handling success
      },
      error: function(xhr, status, error) {
        console.error("Error when calling the detect endpoint:", status, error);
        alarmTriggered = false; // Reset the flag even if there's an error
      }
    });
  }

});

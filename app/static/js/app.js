$(function() {
  $("#boat").draggable({
    containment: "#ocean",
    drag: function(event, ui) {
      createWake(ui.position);
    },
    stop: function(event, ui) {
      checkBuoyCollision(ui.position);
    }
  });

  function createWake(position) {
    var wake = $("<div class='wake'></div>");
    $("#ocean").append(wake);
    wake.css({
      "width": "20px",
      "height": "10px",
      "top": position.top + 10 + "px",
      "left": position.left + 25 + "px"
    }).animate({
      "width": "100px",
      "height": "50px",
      "top": position.top - 15 + "px",
      "left": position.left - 25 + "px",
      "opacity": 0
    }, 3000, function() {
      $(this).remove();
    });
  }

  function checkBuoyCollision(position) {
    var buoyPosition = $(".buoy").position();
    // Simple collision detection
    if (Math.abs(buoyPosition.top - position.top) < 30 &&
        Math.abs(buoyPosition.left - position.left) < 30) {
      runSensorDataAndSoundAlarm();
    }
  }

 function runSensorDataAndSoundAlarm() {
    $.ajax({
        url: '/detect',  // Ensure this URL is reachable from the client
        type: 'GET',
        success: function(data) {
            if (data.alarm_message) {
                alert(data.alarm_message);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error when calling the detect endpoint:", status, error);
        }
    });
}
});

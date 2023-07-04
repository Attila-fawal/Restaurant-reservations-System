/* jshint esversion: 6 */

$(document).ready(function () {

    // Hide the alert after 3 seconds
    setTimeout(function () {
        $(".alert").fadeOut('slow');
    }, 3000); // 3000ms = 3s

    $("#reservationButton, #reservationButton2").click(function (e) {
        e.preventDefault();
        swal({
                title: "Do you have a reservation?",
                icon: "warning",
                buttons: {
                    cancel: "No, I want to book",
                    catch: {
                        text: "Yes",
                        value: "catch",
                    },
                },
            })
            .then((value) => {
                switch (value) {
                    case "catch":
                        window.location.href = "/tables/";
                        break;
                    default:
                        window.location.href = "/reservation/new/";
                }
            });
    });

    // Create a date picker
    $('#id_date').datepicker();

    // Create a time picker
    $('#id_time').timepicker({
        timeFormat: 'hh:mm p'
    });
    $('#id_time').keypress(function (event) {
        event.preventDefault();
    });
});
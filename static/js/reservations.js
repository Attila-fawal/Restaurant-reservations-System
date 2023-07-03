/* jshint esversion: 6 */

$(document).ready(function () {
    console.log('jQuery loaded and document is ready');

    $(document).ready(function () {
        $("#reservationButton, #reservationButton2").click(function (e) {
            e.preventDefault();
            console.log("Button clicked");
            swal({
                    title: "Do you have a reservation?",
                    icon: "warning",
                    buttons: {
                        cancel: "No i want book",
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

});
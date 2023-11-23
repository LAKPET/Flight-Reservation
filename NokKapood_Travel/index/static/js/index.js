$(document).ready(function () {
    // $("#txt_flightDate").datepicker({
    //     dateFormat: "dd/mm/yy",
    // });
    
    $("#btnfindflight").click(function () {
        var start = $("#select_start").find(":selected").attr("value");
        if (start == "Select Airport") {
            alert("กรุณาระบุ สนามบินที่ต้องการขึ้นเครื่อง ");
            return false;
        }

        var goal = $("#select_goal").find(":selected").attr("value");
        if (goal == "Select destination") {
            alert("กรุณาระบุ สนามบินที่ต้องการลงเครื่อง ");
            return false;
        }
        if (goal == start) {
            alert("กรุณาระบุสถานที่บินใหม่อีกครั้ง");
            return false;
        }
        var flightDate = $("#txt_flightDate").val().trim();
        var flightDate = flightDate.slice(0, 10).split("/").reverse().join("-");
        if (flightDate == "") {
            alert("กรุณาระบุวันที่");
            return false;
        }
        var seat_class = $("#seatClass").find(":selected").attr("value");
        if (seat_class == "") {
            alert("โปรดเลือกประเภทที่นั่ง");
            return false;
        }
        // const Url = start + "/" + goal + "/" + flightDate + "/" + seatclass;
        // localStorage.setItem("url",Url);
        window.open("search_flights");
        
    });
});

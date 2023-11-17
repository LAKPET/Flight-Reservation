
var ROW_NUMBER = 4;

$(document).ready( function () {

    /* set up text box inovice data to datepicker, it popup calendar after click text box */
    $("#txt_ReceiptDate").datepicker({ 
        dateFormat: 'dd/mm/yy' 
    });
    
    /* When click button calendar, call datepicker show, it popup calendar after click  button */
    $('#btn_ReceiptDate').click(function() {
        $('#txt_ReceiptDate').datepicker('show');
    });

    /* Add one row to table (in last row), When click button '+' in header of table */
    $('.table-add').click(function () {
        // Copy hidden row of table and clear hidden class
        var clone = $('#div_table').find('tr.hide').clone(true).removeClass('hide table-line');
        // Append copyed row to body of table, add to last row
        $('#div_table').find('tbody').append(clone);
        // Call re_order_no to set item_no
        re_order_no();
    });

    /* Delete row after click 'X' in last column */
    $('.table-remove').click(function () {
        $(this).parents('tr').detach();         // Delete that table row (TR) and all table data (TD)

        // Check number of row, if number of row < 9 then add one row
        // 9 = default row (5) + header (1) + footer (3)
        if ($('#table_main tr').length <= (ROW_NUMBER + 2)) {   
            add_last_one_row();
        }
        re_order_no();                          // Call re_order_no to re-order item_no (order_no)
        re_calculate_total_price();             // Call re_calculate_total_price to calculate  total_price, vat, amount_due
    });

    /* Check input on table are corrected format, if not correct use last value */
    $('table').on('focusin', 'td[contenteditable]', function() {
        $(this).data('val', $(this).html());                    // keep value in table before change
    }).on('keypress', 'td[contenteditable]', function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    }).on('focusout', 'td[contenteditable]', function() {
        var prev = $(this).data('val');                         // get last keep value in table after change
        var data = $(this).html();                              // get changed value
        if (!numberRegex.test(data)) {                          // check changed value correct format Ex 1,000.00
            $(this).text(prev);                                 // if format not correct use last keep value
        } else {
            $(this).data('val', $(this).html());                // if format correct keep this value are last value
        }
        re_calculate_total_price();                             // Call re_calculate_total_price to calculate  total_price, vat, amount_due
    });

    
    /* Get Customer Name when type in text box customer code */
    $('#txt_CustomerCode').change (function () {
        var customer_code = $(this).val().trim();       // get customer_code from text box

        $.ajax({                                        // call backend /customer/detail/<customer_code>
            url:  '/customer/detail/' + customer_code,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                if (data.customers.length > 0) {        // check data not empty customer
                    $('#txt_CustomerCode').val(data.customers[0].customer_code);    // put to text box
                    $('#txt_CustomerName').val(data.customers[0].name);             // put to text box (label)
                } else {
                    $('#txt_CustomerName').val('');    // if can't find customer_name, reset text box
                }
            },
            error: function (xhr, status, error) {
                $('#txt_CustomerName').val('');         // if something error, reset text box
            }
        });
    });


    /* Load customer list to Modal and show popup */
    /* when click button magnifying glass after Customer Code */
    $('.search_customer_code').click(function () {
        $.ajax({
            url:  '/customer/list',                     // call backend /customer/list
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.customers.forEach(customer => {    // loop each result of customers to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${customer.customer_code}</a></td>
                        <td>${customer.name}</td>
                        <td></td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);   // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Customer Code');     // set header of popup
                $('#model_header_2').text('Customer Name');
                $('#model_header_3').text('Note');

                $('#txt_modal_param').val('customer_code');     // mark customer_code for check after close modal
                $('#modal_form').modal();                       // open popup (modal)
            },
        });        
    });

    /* Get payment method when type in text box payment method */
    $('#txt_PaymentMethod').change(function () {
        var payment_method = $(this).val().trim(); // Get the entered customer code
    
        // Make an AJAX request to fetch the payment method for the customer
        $.ajax({
            url: 'payment_method/detail/' + payment_method, // Replace with the actual URL
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.payment_method>0) { // Check if payment method is available
                    $('#txt_PaymentMethod').val(data.payment_method[0].$payment_method); // Set payment method in the input field
                    $('#txt_Description').val(data.payment_methods[0].description);
                } else {
                    $('#txt_Description').val(''); // Clear the input field if payment method is not found
                }
            },
            error: function (xhr, status, error) {
                $('#txt_Description').val(''); // Clear the input field on error
            }
        });
    });

    /* Load customer list to Modal and show popup */
    /* when click button magnifying glass after Customer Code */
    $('.search_payment_method').click(function () {
        $.ajax({
            url:  'payment_method/list',                     // call backend /customer/list
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.paymentmethods.forEach(paymentmethods => {    // loop each result of customers to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${paymentmethods.payment_method}</a></td>
                        <td>${paymentmethods.description}</td>
                        <td></td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);   // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('payment_method');     // set header of popup
                $('#model_header_2').text('description');
                $('#model_header_3').text('Note');

                $('#txt_modal_param').val('payment_method');     // mark customer_code for check after close modal
                $('#modal_form').modal();                       // open popup (modal)
            },
        });        
    });

    /* search product code, load product list to Modal and show popup */
    /* when click button magnifying glass after Product Code in table */
    $('.search_invoice_no').click(function () {
        $(this).parents('tr').find('.order_no').html('*');  // mark row number with '*' for return value after close modal

        $.ajax({                                        // call backend /product/list
            url:  '/invoice/list',
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.invoices.forEach(invoice => {       // loop each result of products to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${invoice.invoice_no}</a></td>
                        <td>${invoice.date}</td>
                        <td>${formatNumber(invoice.amount_due)}</td>
                        <td>${formatNumber(invoice.amount_due)}</td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);       // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Invoice Code');      // set header of popup
                $('#model_header_2').text('Date');
                $('#model_header_3').text('Invoice Full Amount');
                $('#model_header_3').text('Invoice Amount Remain');

                
                $('#txt_modal_param').val('invoice_no');      // mark product_code for check after close modal
                $('#modal_form').modal();                       // open popup
            },
        });
    });

    // Inside the click event handler for 'a.a_click'
    $('body').on('click', 'a.a_click', function () {
        var code = $(this).parents('tr').find('td:nth-child(2)').children().html();
        var name = $(this).parents('tr').find('td:nth-child(3)').html();
        var note = $(this).parents('tr').find('td:nth-child(4)').html();
        var option = $(this).parents('tr').find('td:nth-child(5)').html();
        var option2 = $(this).parents('tr').find('td:nth-child(6)').html();
        var option3 = $(this).parents('tr').find('td:nth-child(7)').html();
        var option4 = $(this).parents('tr').find('td:nth-child(8)').html();
        var option5 = $(this).parents('tr').find('td:nth-child(9)').html();
        var option6 = $(this).parents('tr').find('td:nth-child(10)').html();
    
        if ($('#txt_modal_param').val() == 'invoice_no') {
            // Loop each in data table
            $("#table_main tbody tr").each(function () {
                if ($(this).find('.order_no').html() == '*') {
                    // return selected product detail (code,name,units) to table row
                    $(this).find('.project_code_1 > span').html(code);
                    $(this).find('.invoice_no').html(code);
                    $(this).find('.date').html(name);
                    $(this).find('.invoice_full_amount').html(note);
                    $(this).find('.invoice_amount_remain').html(note);
                    // $(this).find('.amount_paid_here').html(option); // Format the value
                }
                // console.log(amount_paid_here);
            });
            re_calculate_total_price();
        } else if ($('#txt_modal_param').val() == 'customer_code') {
            $('#txt_CustomerCode').val(code);
            $('#txt_CustomerName').val(name);
        } else if ($('#txt_modal_param').val() == 'receipt_no') {
            $('#txt_ReceiptNo').val(code);
            $('#txt_ReceiptDate').val(name);
            $('#txt_CustomerCode').val(note);
            $('#txt_CustomerCode').change();
            $('#txt_PaymentMethod').val(option);
            $('#txt_PaymentMethod').change();
            $("#txt_Remarks").val(option2)
            $('#txt_CustomerName').val(option3);
            $('#txt_CustomerName').change();
            $('#txt_TotalPrice').val(option4);
            $('#txt_TotalPrice').change();
            $('#txt_PaymentReference').val(option5);
            $('#txt_PaymentReference').change();
            $('#txt_Description').val(option6);
            $('#txt_Description').change();
            get_receipt_detail(code);
        } else if ($('#txt_modal_param').val() == 'payment_method') {
            $('#txt_PaymentMethod').val(code);
            $('#txt_Description').val(name);
        }
        $('#modal_form').modal('toggle');
    });
    
    

    // detect modal form closed, call re_order_no
    $('#modal_form').on('hidden.bs.modal', function () {
        re_order_no();
    });

    /* Click button 'NEW', reset form */
    $('#btnNew').click(function () {
        reset_form();
    });


    /* Click button 'EDIT', load invoice list to modal */
    $('#btnEdit').click(function () {
        $.ajax({
            url: '/receipt/list',
            type: 'get',
            dataType: 'json',
            success: function (receiptData) {
                        let rows = '';
                        var i = 1;
                        receiptData.receipts.forEach(receipt => {
                            // loop each result of invoices to create table rows
                            var receipt_date = receipt.date;
                            // Change format date from 01-12-2022 -> 01/12/2022
                            receipt_date = receipt_date.slice(0, 10).split('-').reverse().join('/');
                            rows += `
                                <tr>
                                    <td>${i++}</td>
                                    <td><a class='a_click' href='#'>${receipt.receipt_no}</a></td>
                                    <td>${receipt_date}</td>
                                    <td>${receipt.customer_code_id}</td>
                                    <td class='hide'>${receipt.payment_method}</td>
                                    <td class='hide'>${receipt.remarks}</td>
                                    <td class='hide'>${receipt.customer_code_id__name}</td>
                                    <td class='hide'>${receipt.total_received}</td>
                                    <td class='hide'>${receipt.payment_reference}</td>
                                    <td class='hide'>${receipt.payment_method__description}</td>
                                    <td class='hide'></td>
                                </tr>`;
                                console.log(receipt.total_received);
                        });
                        $('#table_modal > tbody').html(rows);
                        $('#model_header_1').text('Receipt No');
                        $('#model_header_2').text('Receipt Date');
                        $('#model_header_3').text('Customer Code');
                        $('#txt_modal_param').val('receipt_no');
                        $('#modal_form').modal();
            },
        });
    });

    /* Click button 'SAVE', call /invoice/create or /invoice/update */
    $('#btnSave').click(function () {
        var customer_code = $('#txt_CustomerCode').val().trim();    // get customer_code from text box
        if (customer_code == '') {                                  // check customer_code is empty
            alert('กรุณาระบุ Customer');
            $('#txt_CustomerCode').focus();
            return false;
        }
        var receipt_date = $('#txt_ReceiptDate').val().trim();      // get invoice data from text box
        if (!dateRegex.test(receipt_date)) {                        // check invoice data is correct format DD/MM/YYYY
            alert('กรุณาระบุวันที่ ให้ถูกต้อง');
            $('#txt_ReceiptDate').focus();
            return false;
        }

        var payment_method_code = $('#txt_PaymentMethod').val().trim();
        if (payment_method_code == '') {
            alert('กรุณาระบุ Payment Method');
            $('#txt_PaymentMethod').focus();
            return false;
        }
        if ($('#txt_ReceiptNo').val() == '<new>') {                 // check invoice no in form, if invoice no = <new> then call create otherwise call update
            var token = $('[name=csrfmiddlewaretoken]').val();      // get django security code

            $.ajax({                                                // call backend /invoice/create
                url:  '/receipt/create',
                type:  'post',
                data: $('#form_receipt').serialize() + "&lineitem=" +lineitem_to_json(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    console.log(data);
                    if (data.error) {                               // if backend return error message, log it
                        alert('การบันทึกล้มเหลว');
                    } else {
                        $('#txt_ReceiptNo').val(data.receipt.receipt_no)    // SAVE success, show new invoice no
                        alert('บันทึกสำเร็จ');
                    }                    
                },
            });  
        } else {
            var token = $('[name=csrfmiddlewaretoken]').val();      // get django security code

            $.ajax({                                                // call backend /invoice/update
                url:  '/receipt/update',
                type:  'post',
                data: $('#form_receipt').serialize() + "&lineitem=" +lineitem_to_json() + "&receipt_no=" + $('#txt_ReceiptNo').val(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    if (data.error) {                       // if backend return error message, log it
                        console.log(data.error);
                        alert('การบันทึกล้มเหลว');
                    } else {            
                        alert('บันทึกสำเร็จ');                      // SAVE success, show popup message
                    }
                },
            }); 
        }
    });

    /* Click button 'DELETE', call backend /invoice/delete */
    $('#btnDelete').click(function () {
        if ($('#txt_ReceiptNo').val() == '<new>') {
            alert ('ไม่สามารถลบ Receipt ใหม่ได้');
            return false;
        }
        if (confirm ("คุณต้องการลบ Receipt No : '" + $('#txt_ReceiptNo').val() + "' ")) {
            console.log('Delete ' + $('#txt_ReceiptNo').val());
            var token = $('[name=csrfmiddlewaretoken]').val();          // get django security code
            $.ajax({                                                    // call backend /invoice/delete
                url:  '/receipt/delete',
                data: 'receipt_no=' + $('#txt_ReceiptNo').val(),
                type:  'post',
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    reset_form();                                       // after delete success call reset_form
                },
            });            
        }
    });

    /* Click button 'PRINT', open new tab of browser with /receipt/reprot/<receipt_no> */
    $('#btnPrint').click(function () {
        if ($('#txt_ReceiptNo').val() == '<new>') {
            return false;
        }
        window.open('/receipt/report/' + $('#txt_ReceiptNo').val());
    });

    /* Start from */
    reset_form ();
});

/* read all data inside table and convert to json string */
/* return json string of line item (all data inside table) */
function lineitem_to_json () {
    var rows = [];                                                  // create empty array 'rows'
    var i = 0;
    $("#table_main tbody tr").each(function(receipt) {                // loop each table data
        if ($(this).find('.project_code_1 > span').html() != '') {  // check row have data
            rows[i] = {};                                           // create empty object in rows[index]
            rows[i]["item_no"] = (i+1);                             // copy data from table row to variable 'rows'
            rows[i]["invoice_no"] = $(this).find('.project_code_1 > span').html();
            rows[i]["amount_paid_here"] = $(this).find('.amount_paid_here').html();
            rows[i]["date"] = $(this).find('.date').html();
            rows[i]["amount_due"] = $(this).find('.invoice_no__amount_due').html();
            rows[i]["invoice_full_amount"] = $(this).find('.invoice_no__amount_due').html();
            rows[i]["invoice_amount_remain"] = $(this).find('.invoice_no__amount_due').html();
            i++;
        }
    });
    print(lineitem_to_json)
    var obj = {};                                                   // create empty object
    obj.lineitem = rows;                                            // assign 'rows' to object.lineitem

    return JSON.stringify(obj);                                     // return object in JSON format
}

/* get invoice detail from backend with invoice_no and fill to the form */
function get_receipt_detail (receipt_no) {
    $.ajax({                                                            // call backend /invoice/detail/IN100/22
        url:  '/receipt/detail/' + encodeURIComponent(receipt_no),
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            console.log(data);
            reset_table();                                              // reset table
            for(var i=ROW_NUMBER;i<data.receiptlineitem.length;i++) {   // generate row by number of result
                add_last_one_row();
            }
            var i = 0;
            $("#table_main tbody tr").each(function() {                 // fill result data to each row
                if (i < data.receiptlineitem.length) {
                    $(this).find('.project_code_1 > span').html(data.receiptlineitem[i].invoice_no);
                    $(this).find('.date').html(data.receiptlineitem[i].invoice_no__date);
                    $(this).find('.invoice_full_amount').html(data.receiptlineitem[i].invoice_no__amount_due);
                    $(this).find('.invoice_amount_remain').html(data.receiptlineitem[i].invoice_no__amount_due);          
                    $(this).find('.amount_paid_here').html(data.receiptlineitem[i].amount_paid_here);
                    
                }
                i++;
            });
            re_calculate_total_price();                                 // re-calculate total_price, vat, amount due
        },
    });
}

/* Loop each data table and calculate extended_price, total_price, vat, amount due */
function re_calculate_total_price() {
    var total_price = 0;

    // Loop through each row in the Data Table
    $("#table_main tbody tr").each(function () {
        var amount_paid_here = $(this).find('.amount_paid_here').text().replace(/,/g, '');
        $(this).find('.amount_paid_here').html(formatNumber((amount_paid_here)));
    //     // Convert the amount_due to a numeric value
        var price = parseFloat(amount_paid_here);
        

    //     // Check if the conversion is successful and the value is a number
        if (!isNaN(price)) {
            // Add the numeric value to the total_price
            total_price += price;
        }
    });

    // Update the total_price label and input field
    $('#lbl_TotalPrice').text(formatNumber(total_price));
    $('#txt_TotalPrice').val($('#lbl_TotalPrice').text());
    $('#txt_TotalPrice1').val($('#lbl_TotalPrice').text());
}
// // function re_calculate_total_price () {
// //     var total_price = 0;

// //     // Loop each in Data Table
// //     $("#table_main tbody tr").each(function() {
// //         var project_code = $(this).find('.project_code_1 > span').html().trim();
// //         var amount_due = $(this).find('.amount_due').html().trim();
// //         $(this).find('.invoice_full_amount').html(parseInt(amount_due));
// //         var amount_paid_here = $(this).find('.amount_paid_here').html().trim();
// //         $(this).find('.amount_paid_here').html(formatNumber((amount_paid_here)));

            
// //         if (project_code != '') {
// //             var invoice_amount_remain = invoice_full_amount - amount_paid_here;
// //             $(this).find('.invoice_amount_remain').html(formatNumber(invoice_amount_remain));
// //             total_price += parseInt(amount_paid_here);
// //         }
// //     });

//     $('#lbl_TotalReceived').text(formatNumber(total_price));
//     $('#txt_TotalReceived').val($('#lbl_TotalReceived').text());
// }


/* Reset form to original form */
function reset_form() {
    $('#txt_ReceiptNo').attr("disabled", "disabled");
    $('#txt_ReceiptNo').val('<new>');

    reset_table();
    $('#txt_TotalPrice1').val('');
    $('#txt_ReceiptDate').val(new Date().toJSON().slice(0,10).split('-').reverse().join('/'));
    $('#txt_CustomerCode').val('');
    $('#txt_CustomerName').val('');
    $('#txt_PaymentMethod').val('');
    $('#txt_PaymentReference').val('');
    $('#txt_Remarks').val('');
    $('#txt_Description').val('');
    $('#txt_TotalPrice').val('');
    $('#lbl_TotalPrice').text('0.00');
    $('#txt_TotalPrice').text('0.00');
    $('#lbl_VAT').text('0.00');
    $('#lbl_AmountDue').text('0.00');
}

/* Reset Table to original from */
function reset_table() {
    $('#table_main > tbody').html('');          // Clear body of table (tbody), table will remain header and footer
    for(var i=1; i<= ROW_NUMBER; i++) {         // Loop 5 times
        add_last_one_row()                      // Add one row to table
    }    
}

/* Add one row to table */
function add_last_one_row () {
    $('.table-add').click();                    // Call event click of button '+' in header of table, for add one row
}

/* Reorder number item_no (order_no) on table */
function re_order_no () {
    var order_number = 1;
    // Loop each data table
    $("#table_main tbody tr").each(function() {         
        // set order number to column order_no
        $(this).find('.order_no').html(order_number);   
        order_number++;
    });
}

/* Format input to display number 2 floating point Ex 1,000.00 */
function formatNumber (num) {
    if (num === '') return '';
    num = parseFloat(num); 
    return num.toFixed(2).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
}

/* Check n is integer */
function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

/* Check n is floating point */
function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

/* Pattern for check input is Date format DD/MM/YYYY */
var dateRegex = /^(?=\d)(?:(?:31(?!.(?:0?[2469]|11))|(?:30|29)(?!.0?2)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:\x20|$))|(?:2[0-8]|1\d|0?[1-9]))([-.\/])(?:1[012]|0?[1-9])\1(?:1[6-9]|[2-9]\d)?\d\d(?:(?=\x20\d)\x20|$))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$/;
//var numberRegex = /^-?\d+\.?\d*$/;

/* Pattern for check input is Money format 1,000.00 */
var numberRegex = /^-?\d*\.?\d*$/

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;


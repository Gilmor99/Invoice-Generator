function addTableRow() {
    // function to add new line items row to the invoice
    var table = document.getElementById("lineItemsTable");
    var row = table.insertRow(1);
    var description = row.insertCell(0);
    addInput(description, 'description');
    var quantity = row.insertCell(1);
    addInput(quantity, 'quantity');
    var rate = row.insertCell(2);
    addInput(rate, 'rate');
    var amount = row.insertCell(3);
    addInput(amount, 'amount');

}
function addInput(elm, name) {
    // function to append the new row to the line items table
    var input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('size', '10');
    if (name==='amount'){
        input.setAttribute('class', 'form-control right')
    }
    else {
        input.setAttribute('class', 'form-control')
    }
    input.setAttribute('name', name);
    input.setAttribute('id', name);
    elm.appendChild(input);
}


function tableTotals() {
    // JQUERY function to calculate the each line items amoun and sub-total
    $('#amount, #subTotal').prop('readonly', true);
    var $tblrows = $('#lineItemsTable tbody tr');
    var grandTotal = 0;
    $tblrows.each(function (index) {
        var $tblrow = $(this);
        var qty = $tblrow.find('[name=quantity]').val();
        var rate = $tblrow.find('[name=rate]').val();
        var amount = parseInt(qty, 10) * parseFloat(rate);
        if (!isNaN(amount)) {
            $tblrow.find('#amount').val(amount.toFixed(2));
        }
        var stval = parseFloat($tblrow.find('#amount').val());
        grandTotal += isNaN(stval) ? 0 : stval;
    });
    $('#subTotal').val(grandTotal.toFixed(2));
}

function totalDiscounts() {
    // JQUERY function to calculate the total discount amount within the invoice
    $('#totalDiscount').prop('readonly', true);
    var tDiscount = $("#totalDiscount").val();
    var dis = isNaN($('#discount').val()) ? 0 : $('#discount').val();
    var disflag = $('#discountFlag option:selected').val();
    var subTotal = isNaN($('#subTotal').val()) ? 0 : $('#subTotal').val();
    if (disflag === 'D') {
        $('#totalDiscount').val(parseInt(dis).toFixed(2));
    }
    else {
        tDiscount = parseFloat(dis) * parseFloat(subTotal) / 100;
        $('#totalDiscount').val(tDiscount.toFixed(2));
    }
}

function totalTaxes() {
    // JQUERY function to calculate the total Tax amount within the invoice
    $('#totalTax').prop('readonly', true);
    var tTax = $("#totalTax").val();
    var t = isNaN($('#tax').val()) ? 0 : $('#tax').val();
    var tflag = $('#taxFlag option:selected').val();
    var subTotal = isNaN($('#subTotal').val()) ? 0 : $('#subTotal').val();
    if (tflag === 'D') {
        $('#totalTax').val(parseInt(t).toFixed(2));
    }
    else {
        tTax = parseFloat(t) * parseFloat(subTotal) / 100;
        $('#totalTax').val(tTax.toFixed(2));
        }
}

function totals() {
    // JQUERY function to calculate the totals of the invoice
    $('#total, #balanceDue').prop('readonly', true);
    var tax = parseInt($('#totalTax').val(), 10) || 0;
    var dis = parseInt($('#totalDiscount').val(), 10) || 0;
    var subTotal = parseInt($('#subTotal').val(), 10) || 0;
    var shipping = parseInt($('#shipping').val(), 10) || 0;
    var paid = parseInt($('#amountPaid').val(), 10) || 0;
    var total = subTotal - dis + tax + shipping;
    if (!isNaN(total)) {
        $('#total').val(total.toFixed(2));
    }
    var balance = total - paid;
    if (!isNaN(total)) {
        $('#balanceDue').val(balance.toFixed(2));
    }
}

function setFlag() {
    // JQUERY function to set the right chosice of either
    // precentage or flat rate for both the Discount and Tax amounts
    var dFlag = '{{invoice.discountFlag}}';
     if ( dFlag === 'D') {
         document.getElementById('discountFlag').value = 'D';
     }
     else {
         document.getElementById('discountFlag').value = 'P';
     }
     var tFlag = '{{invoice.taxFlag}}';
     if ( tFlag === 'D') {
         document.getElementById('taxFlag').value = 'D';
     }
     else {
         document.getElementById('taxFlag').value = 'P';
     }
}

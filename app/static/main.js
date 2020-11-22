document.getElementById("itemadd").addEventListener("click", add_item);
document.getElementById("itempop").addEventListener("click", pop_item);
document.getElementById('receiptdate').valueAsDate = new Date();

var items = 1;

function add_item() {
    jQuery("#itemform").clone().appendTo("#bodyreceipt").attr('id', 'item_' + items);
    items = items + 1;
};

function pop_item() {
    if (items > 1) {
        items = items - 1;
        jQuery("#item_" + items).remove();
    }
};
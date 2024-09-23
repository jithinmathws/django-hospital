document.getElementById('btnTab').addEventListener('click', this.openTab);
    function openTab(ev) {
        console.log('open a tab');
        let win = window.open('{% url 'Invoiceindex' %}', null);
        win.onload = (ev) => {
                
            setTimeout(() => {
                win.close();
                }, 2500);
            };
        };
    

    $(document).ready(function(){
        // calculating discount amount from percentage
        $('#id_discount_percentage').on('change', function(){
            var perc = $(this).val()
                perc = perc > 0 ? perc : 0;

            var sub_total =  $('#id_subtotal_amount').val()
            
            var disc = parseFloat(perc / 100) * parseFloat(sub_total) ;
            $('#id_discount_amount').val(disc.toFixed(3))
            calc_total()
        })
    
        // calculating discount amount from percentage
        $('#id_tax_percentage').on('change', function(){
            var perc = $(this).val()
                perc = perc > 0 ? perc : 0;

            var sub_total =  $('#id_subtotal_amount').val()
            
            var tax = parseFloat(perc / 100) * parseFloat(sub_total) ;
            $('#id_tax_amount').val(tax.toFixed(3))
            calc_total()
        
        })

        function calc_total(){
            var sub_total =  $('#id_subtotal_amount').val()
            var disc =  $('#id_discount_amount').val()
            var tax =  $('#id_tax_amount').val()

            var total = (parseFloat(sub_total) - parseFloat(disc)) + parseFloat(tax)
            $('#id_adjusted_amount').val(total.toFixed(3))
        }
})
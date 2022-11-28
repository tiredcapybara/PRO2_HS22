$('#freeavfw').change(function(){

    // jquery shorthand conditioning statement. If true use link1 if not use link2.
    var c = this.checked ? 'link1' : 'link2';

    // change the href attribute for the element ID = download to the value stored in 'c'.
    $('#download').attr("href", c);
});
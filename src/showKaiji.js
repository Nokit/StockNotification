(function(){
    'use strict';
    function ShowKaiji(){
	var now = new Date();
	var fileName = "getTdnet/Tdnet-rss/Tdnet-rss-"+now.getFullYear().toString()+(now.getMonth()+1).toString()+now.getDate().toString()+".xml"; 
	document.getElementById('Data').innerText = fileName;	
    }

    document.getElementById('contents').textContent = "getTdnet/Tdnet-rss/Tdnet-rss-20181125.xml";
    ShowKaiji();
})();

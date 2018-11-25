(function(){
    'use strict';
    function ShowTime(){
	var now = new Date();
	var fileName = "Tdnet-rss-"+now.getFullYear().toString()+(now.getMonth()+1).toString()+now.getDate().toString()+".xml" 
	document.getElementById('Data').innerText = fileName;	
    }
    setInterval(ShowTime, 50);
})();

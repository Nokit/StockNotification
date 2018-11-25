(function(){
    'use strict';
    function ShowTime(){
	 var now = new Date();
	 document.getElementById('Data').innerText = now.getFullYear().toString()+(now.getMonth()+1).toString()+now.getDate().toString();
    }
    setInterval(ShowTime, 50);
})();

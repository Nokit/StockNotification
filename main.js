(function(){
    'use strict';
    function ShowTime(){
	 var now = new Date();
	 document.getElementById('Time').innerText = now;
    }
    setInterval(ShowTime, 50);
})();

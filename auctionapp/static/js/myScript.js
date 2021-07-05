     $(document).ready(function() {
         slideShow();
	 });

	 function slideShow() {
		var showing = $('.slider .is-showing');
		var next = showing.next().length ? showing.next(): showing.parent().children(':first');
		/*
		  * We could have written the above statement the long way to achieve the same results
		  *
		  * if(showing.next().length {
		  *		 showing.next();
		  * } else {
		  *     showing.parent().children(':first');
		  * }
		  */


	 showing.fadeOut(800, function() { next.fadeIn(800).addClass('is-showing'); }).removeClass('is-showing');

	 setTimeout(slideShow, 5000);

}

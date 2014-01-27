//object with functions
var functions = {
	alert: function(){
	alert("chamou");
	},

//change the position of the footer tag
resize: function (){
	var	winHeight = $(window).innerHeight(),
	contentHeight = $("#content").height(),
	headerHeight = $("header").height(),
	bodyHeight = $("body").height(),
	footerHeight = $("footer").height();

	if(winHeight > ( headerHeight + contentHeight + footerHeight )){
		$("footer").css("margin-top",( winHeight - (bodyHeight + 10 )) + "px");
	}
	else{
		$("footer").css("margin-top","0px");
	}
	},	
		selectedItem:function(elem){
		return $(elem).hasClass("selected");
	},
		removeSelected:function(elem){
		$(elem).removeClass("selected");
		$(elem).trigger("mouseleave");
	},
		addSelected:function(elem){
		$(elem).addClass("selected");
	}
}

$(document).ready(function(){
	functions.resize();
	$("aside div:first-child div.flex").click(function(){
	var items = $("aside div:first-child div.flex"),
	$this = $(this);

	if(! functions.selectedItem($this)){
	for (var i = 0; i < items.length; i++) {
	if($(items[i]).hasClass("selected")){
		functions.removeSelected($(items[i]));
		functions.addSelected($this);
	}
	}
	}
	}).mouseover(function(){
		var $this = $(this);
		if(! functions.selectedItem($this)){
			$(this).css("color","gray");
			$(this).children(".row").css("border-color","gray");
		}
		}).mouseleave(function(){
			var $this = $(this);
			if(! functions.selectedItem($this)){
				$(this).css("color","white");
				$(this).children(".row").css("border-color","white");
			}
			});

		});
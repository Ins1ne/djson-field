$(document).ready(function(e){
	$('.jsonFieldWidget').delegate('.jsonFieldAddLink a', 'click', function(e){
		e.preventDefault();
		var list = $(this).parent().parent();
		var last = list.children('.jsonFieldItem').last();
		isLabel = true;
		if(list.hasClass('jsonFieldDict')){
			var key = prompt("Введите ключ");
			var name = list.attr('name') + '[_' + key + ']';
		} else {
			var key = 0;
			if(last && last.length>0){
				var indexes = getKeys(last.children('.jsonFieldItemValue').attr('name'));
				if(indexes && indexes.length > 0)
					key = parseInt(indexes.pop()) + 1;
			}
			isLabel = false;
			var name = list.attr('name') + '[' + key + ']';
		}
		var label = "<label>" + key + "</label>";
		if($(this).hasClass("plain")){
			var item = $('.jsonFieldWidget').has($(this)).find(".templates>.plain").html().replace(/%%NAME%%/g, name);
		} else if($(this).hasClass("list")){
			var item = $('.jsonFieldWidget').has($(this)).find(".templates>.list").html().replace(/%%NAME%%/g, name);
		} else if($(this).hasClass("dict")){
			var item = $('.jsonFieldWidget').has($(this)).find(".templates>.dict").html().replace(/%%NAME%%/g, name);
		}

		var li = "<li class=\"jsonFieldItem\">" +
					'<a href="#" class="deleteItem">Удалить</a> ' +
					(isLabel ? label : "") + item + 
					'</li>';
		$(this).parent().before(li);
	});
	$('.jsonFieldWidget').delegate('.jsonFieldItem>.deleteItem', 'click', function(e){
		e.preventDefault()
		$(this).parent().remove();
	});
});

function getKeys(str){
	keys = str.match(/\[[a-zA-Z0-9_.]+\]/g);
	if(keys && keys.length > 0){
		for(var i=0; i<keys.length; i++) keys[i] = keys[i].slice(1,-1);
	}
	return keys
}
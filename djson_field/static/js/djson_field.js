django.jQuery(document).ready(function(e){
	django.jQuery(document).delegate('.jsonFieldWidget .jsonFieldAddLink a', 'click', function(e){
		e.preventDefault();
		var list = django.jQuery(this).parent().parent();
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
		if(key==null) return null;
		var label = "<label>" + key + "</label>";
		var templates = getTemplates(list);
		if(templates.size() > 0){
			if(django.jQuery(this).hasClass("add_plain")){
				var item = templates.children(".plain").html().replace(/%%NAME%%/g, name);
				item = item.replace('_name="', 'name="')
			} else if(django.jQuery(this).hasClass("add_list")){
				var item = templates.children(".templates>.list").html().replace(/%%NAME%%/g, name);
			} else if(django.jQuery(this).hasClass("add_dict")){
				var item = templates.children(".templates>.dict").html().replace(/%%NAME%%/g, name);
			}
			var li = "<li class=\"jsonFieldItem\">" +
				(isLabel ? label : "") +
				item + '</li>';
			django.jQuery(this).parent().before(li);
		} else {
			alert("Не удалось найти шаблон для сущности");
		}
	});
	django.jQuery(document).delegate('.jsonFieldWidget .jsonFieldItem>.deleteItem', 'click', function(e){
		e.preventDefault()
		django.jQuery(this).parent().remove();
	});
	django.jQuery(document).delegate('.jsonFieldWidget .jsonFieldItem>.keyField>*', 'change', updateNames);
	django.jQuery(document).delegate('.jsonFieldWidget .jsonFieldItem>.keyField>*', 'keyup', updateNames);
});

function updateNames(e){
	var cur_name = django.jQuery(this).attr('name').substring(2);
	var new_name = cur_name.replace(/\[_[^\]]*\]django.jQuery/g, '[_' + django.jQuery(this).val() + ']');
	console.log("cur_name: ", cur_name);
	console.log("new_name: ", new_name);
	django.jQuery(this).attr('value', django.jQuery(this).val());
	html = django.jQuery(this).parent().parent().html().split(cur_name).join(new_name);
	django.jQuery(this).parent().parent().html(html);
	var key_element = django.jQuery('*[name="__' + new_name + '"]');
	key_element.focus().val(key_element.val())
}

function getTemplates(node){
	var templates = node.children('.templates');
	if(templates.size() > 0) return templates;
	var parent = node.parent();
	if(parent.size() > 0) return getTemplates(parent);
	return null;
}

function getKeys(str){
	keys = str.match(/\[[a-zA-Z0-9_.]+\]/g);
	if(keys && keys.length > 0){
		for(var i=0; i<keys.length; i++) keys[i] = keys[i].slice(1,-1);
	}
	return keys
}
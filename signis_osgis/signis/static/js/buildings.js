function buildings_insert(){
	//it will be necessary to check the values of the form before
	//send it to the server
	var str_json=lib_jsForms_formToJSONString('tabla.zonas_metro');
	var data='pk_name=gid&form_data=' + str_json;
	lib_myAjax_myAjax('POST', URL_APP + 'building_insert/', data, general_updateMessage);//insert the record
}
function buildings_update(){
	
}

function buildings_delete(){
	
}	

function buildings_getBuildingByGid(){
	var form = document.getElementById("formGetBuilding");
	var gid= form.elements["gid"].value;
	var data='gid='+ gid;
	lib_myAjax_myAjax('GET', URL_APP + 'building_select/', data, buildings_fillFormBuilding);
}	

function buildings_fillFormBuilding(json_answer){
	var objJson=$.parseJSON(json_answer);
	var data=objJson.data;
	var row = data[0];
	lib_jsForms_loadValuesForm('tabla.zonas_metro',row);
	main_showDivFormBuildings();
	
	var obj_div=document.getElementById('div_message');
	var obj_p = document.getElementById('p_message');
	var cont;
	if (objJson.ok) {
		cont='<strong>Successfully!</strong> ' + objJson.message
		obj_div.className = "alert alert-success";
	}else{
		cont='<strong>Problem!</strong> ' + objJson.message
		obj_div.className = "alert alert-warning";
	}
	obj_p.innerHTML=cont;
}
/**
 * Created on 25 feb. 2017
 * @author: Gaspar Mora-Navarro
 * Department of Cartographic Engineering Geodesy and Photogrammetry
 * Higher Technical School of Geodetic, Cartographic and Topographical Engineering
 * joamona@cgf.upv.es
 */

/**
 * Returns a json with all the inputs of the form
 * geom can be true or false
 * 		if is false then the fieds 'type' and 'coordinates' NOT will be added
 * 		The default is true. If not is passed will be true*/
function lib_jsForms_formToJSONString(id_form, geom) {
	if (geom === undefined) {
        // geom was not passed
		geom=true;
    }
	var form = document.getElementById(id_form);
	var obj = {};
	var elements = form.querySelectorAll( "input, select, textarea" );
	for( var i = 0; i < elements.length; ++i ) {
		var element = elements[i];
		var name = element.name;
		var value = element.value;

		if( name ) {
			if (geom==false){
				if ((name=='coordinates') || (name=='type')){
					//no hace nada
				}else{
					obj[ name ] = value;
				}
			}else{
				obj[ name ] = value;
			}
		}
	}
	return JSON.stringify( obj );
}


/**
 * Returns a string with all the inputs of the form
 * geom can be true or false
 * if is false then the fieds 'type' and 'coordinates' NOT will be added
 * The default is true. If not is passed will be true*/
function lib_jsForms_formToJSONStringFields(id_form, geom) {
	if (geom === undefined) {
        // geom was not passed
		geom=true;
    }
	var form = document.getElementById(id_form);
	var obj = {};
	var elements = form.querySelectorAll( "input, select, textarea" );
	var campos="";
	for( var i = 0; i < elements.length; ++i ) {
		var element = elements[i];
		var name = element.name;

		if( name ) {
			if (geom==false){
				if ((name=='coordinates') || (name=='type')){
					//no hace nada
				}
			}else{
				campos=campos + ", " + name;
			}
		}
	}
	return campos.substring(1);//returns all except the first character. Eliminates the tirs ','
}

/**
* Loads the form whit the data
* @method load_values_form
* @param {str} id_form - string with the id property value of the form
* @param {obj} reccord_obj - object which properties are the values to fill the form.
* 		The property names must match with the id of the input controls of the form.
* 		
* 		If the obj has a geometry has to be in the st_geojson field of the reccord_obj.
* 		This function extract the vector geometry coordinates, transform them into 'x,y,x,y, ...'
* 		and put it into the geom texbox of the form.
* @return none
*/
function lib_jsForms_loadValuesForm(id_form,reccord_obj){
	var form = document.getElementById(id_form);
	$.each(reccord_obj, function( key, val ) {
		if (key=='st_asgeojson'){
			var objGeoJson=$.parseJSON(val);
			var coordinates=objGeoJson.coordinates[0];
			var strCoordinates= lib_jsForms_vectorCoordinatesToString(coordinates);
			form.elements.namedItem('geom').value=strCoordinates;
		}
		else{
			form.elements.namedItem(key).value=val;
		}
	}); 
}

/**
* Returns a string coordinates
* @method lib_jsForms_vectorCoordinatesToString
* @param {vector} vectorCoordinates - Vector coordinates to transform: [[x, y],[x, y], ...]
* @return string - 'x,y,x,y,...'
*/
function lib_jsForms_vectorCoordinatesToString(vectorCoordinates){
	var s="";
	var np=vectorCoordinates.length;
	for (var i = 0; i < np; i ++){
		var pt=vectorCoordinates[i];
		s=s+pt[0].toString() + "," + pt[1].toString() + ",";
	}
	var n=s.length;
	return s.substring(0, n-1);//remove the final comma	
}

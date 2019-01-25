


$(function() {

    // INIT INCIDENCIAS FINAL
    function buttonInsertIncidencias(){
        console.log('buttonInsertIncidenciasAction');
       $.ajax({
           url: 'http://localhost:5000/insertIncidencias/',
           data: $('form').serialize(),
           type: 'POST',
           success: function(response){
           var data = JSON.parse(response)['data'];
           var message = JSON.parse(response)['message'];
               console.log(data);
               console.log(message);
               
               $('#dataInsertIncidencias').html(JSON.stringify(message,null,4));
               
           },
           error: function(error){
               console.log(error);
           }
       });
   
   };
   // END INCIDENCIAS FINAL

    // Select Placas
    $('#buttonSelectPlacasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/selectPlacas/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
                console.log(data);
                var message = JSON.parse(response)['message'];
                lib_jsForms_loadValuesForm("dataSelectPlacas2",data);
                $('#dataSelectPlacas').html(JSON.stringify(message,null,4));
                /*
                $('#dataSelect').append('<tr>');
                for (var clave in data) {
                    $('#dataSelect').append('<th>'+clave+'</th>');
                    //console.log(data[clave]); <td>'+data[clave]+'</td>
                }
                $('#dataSelect').append('</tr>');
                
                $('#dataSelect').append('<tr>');
                for (var clave in data) {
                    $('#dataSelect').append('<td>'+data[clave]+'</td>');
                }
                $('#dataSelect').append('</tr>');
                */
                    
                
            },
            error: function(error){
                console.log(error);
                $('#dataSelectPlacas').html('Error');
            }
        });
    
    });
    
    // Function para Incidencias SELECT
    $('#buttonSelectIncidenciasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/selectIncidencias/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                lib_jsForms_loadValuesForm("dataSelectIncidencias2",data);
                $('#dataSelectIncidencias').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
                $('#dataSelectIncidencias').html('Error');
            }
        });
    
    });
    // Function para Zonasmetro SELECT
    $('#buttonSelectZonasmetroAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/selectZonasmetro/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                
                lib_jsForms_loadValuesForm("dataSelectZonasmetro2",data);
                $('#dataSelectZonasmetro').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
                $('#dataSelectZonasmetro').html('Error');
            }
        });
    
    });
    // Function para Incidencias SELECT
    $('#buttonInsertPlacasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/insertPlacas/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                console.log(message);
                
                $('#dataInsertPlacas').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
     $('#buttonInsertIncidenciasAction').click(function(){
         console.log('buttonInsertIncidenciasAction');
        $.ajax({
            url: 'http://localhost:5000/insertIncidencias/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                console.log(message);
                
                $('#dataInsertIncidencias').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
     $('#buttonInsertZonasmetroAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/insertZonasmetro/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                console.log(message);
                
                $('#dataInsertZonasmetro').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
    
    $('#buttonUpdatePlacasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/updatePlacas/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                console.log(message);
                
                $('#dataUpdatePlacas').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
    
    $('#buttonUpdateIncidenciasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/updateIncidencias/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['data'];
            var message = JSON.parse(response)['message'];
                console.log(data);
                console.log(message);
                
                $('#dataUpdateIncidencias').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });

    $('#buttonUpdateZonasmetroAction').click(function(){
            $.ajax({
                url: 'http://localhost:5000/updateZonasmetro/',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response){
                var data = JSON.parse(response)['data'];
                var message = JSON.parse(response)['message'];
                    console.log(data);
                    console.log(message);
                    
                    $('#dataUpdateZonasmetro').html(JSON.stringify(message,null,4));
                    
                },
                error: function(error){
                    console.log(error);
                }
            });
        
        });
        
        $('#buttonDeletePlacasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/deletePlacas/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['message'];
                console.log(data);
                
                $('#dataDeletePlacas').html('Row deleted');
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
    $('#buttonDeleteIncidenciasAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/deleteIncidencias/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['message'];
                console.log(data);
                
                $('#dataDeleteIncidencias').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
    $('#buttonDeleteZonasmetroAction').click(function(){
        $.ajax({
            url: 'http://localhost:5000/deleteZonasmetro/',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
            var data = JSON.parse(response)['message'];
                console.log(data);
                
                $('#dataDeleteZonasmetro').html(JSON.stringify(message,null,4));
                
            },
            error: function(error){
                console.log(error);
            }
        });
    
    });
    
    function lib_jsForms_loadValuesForm(id_form,reccord_obj){
    var form = document.getElementById(id_form);
    $.each(reccord_obj, function( key, val ) {
        if (key=='st_asgeojson'){
            var objGeoJson=$.parseJSON(val);
            var coordinates=objGeoJson.coordinates;
            console.log(coordinates);
            var strCoordinates= lib_jsForms_vectorCoordinatesToString(coordinates);
            form.elements.namedItem('st_asgeojson').value=strCoordinates;
        }
        else{
            form.elements.namedItem(key).value=val;
        }
    }); 
}

function lib_jsForms_vectorCoordinatesToString(vectorCoordinates){
    var s="";
    var np=vectorCoordinates.length;
    console.log(np);
    console.log(vectorCoordinates);
    if (np > 2) {
        for (var i = 0; i < np; i ++){
            var pt=vectorCoordinates[i];
            console.log(pt);
            s=s+pt[0].toString() + "," + pt[1].toString() + ",";
            console.log(s);
        }
        var n=s.length;
        return s.substring(0, n-1);//remove the final comma 
    } else {
        if (np==2) {
            var pt2=vectorCoordinates;
            console.log(pt2);
            s=s+pt2[0].toString() + "," + pt2[1].toString() + ",";
            console.log(s);
            var n2=s.length;
            return s.substring(0, n2-1);//remove the final comma 
        } else {
            console.log('Polygon');
            var vectorCoordinates2 = vectorCoordinates[0];
            var np2 = vectorCoordinates2[0].length;
            console.log(vectorCoordinates2, np2);
            for (var j = 0; j < np2*2; j ++){
                var pt3=vectorCoordinates2[j];
                console.log(pt3);
                s=s+pt3[0].toString() + "," + pt3[1].toString() + ",";
                console.log(s);
            }
            var n3=s.length;
            return s.substring(0, n3-1);//remove the final comma 
        }
        
    }
    
    
}

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
    
});

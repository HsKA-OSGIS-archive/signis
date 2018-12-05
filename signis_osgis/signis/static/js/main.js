// Funciones para capa Placas
function main_showDivPlacas(){
   //document.getElementById("sectionPlacas").style.display = "block";
   //document.getElementById("sectionIncidencias").style.display = "none";
   //document.getElementById("sectionZonasmetro").style.display = "none";
   document.getElementById("sectionPlacas").style.display = "block";
}
function main_showFormSelectPlacas(){
   document.getElementById("formSelectPlacas").style.display = "block";
   document.getElementById("formInsertPlacas").style.display = "none";
   document.getElementById("formUpdatePlacas").style.display = "none";
   document.getElementById("formDeletePlacas").style.display = "none";
}
function main_showFormInsertPlacas(){
   document.getElementById("formSelectPlacas").style.display = "none";
   document.getElementById("formInsertPlacas").style.display = "block";
   document.getElementById("formUpdatePlacas").style.display = "none";
   document.getElementById("formDeletePlacas").style.display = "none";
}
function main_showFormUpdatePlacas(){
   document.getElementById("formSelectPlacas").style.display = "none";
   document.getElementById("formInsertPlacas").style.display = "none";
   document.getElementById("formUpdatePlacas").style.display = "block";
   document.getElementById("formDeletePlacas").style.display = "none";
}
function main_showFormDeletePlacas(){
   document.getElementById("formSelectPlacas").style.display = "none";
   document.getElementById("formInsertPlacas").style.display = "none";
   document.getElementById("formUpdatePlacas").style.display = "none";
   document.getElementById("formDeletePlacas").style.display = "block";
}


// Funciones para capa Incidencias
function main_showDivIncidencias(){
   //document.getElementById("sectionPlacas").style.display = "none";
   document.getElementById("sectionIncidencias").style.display = "block";
   //document.getElementById("sectionZonasmetro").style.display = "none";
}
function main_showFormSelectIncidencias(){
   document.getElementById("formSelectIncidencias").style.display = "block";
   document.getElementById("formInsertIncidencias").style.display = "none";
   document.getElementById("formUpdateIncidencias").style.display = "none";
   document.getElementById("formDeleteIncidencias").style.display = "none";
}
function main_showFormInsertIncidencias(){
   document.getElementById("formSelectIncidencias").style.display = "none";
   document.getElementById("formInsertIncidencias").style.display = "block";
   document.getElementById("formUpdateIncidencias").style.display = "none";
   document.getElementById("formDeleteIncidencias").style.display = "none";
}
function main_showFormUpdateIncidencias(){
   document.getElementById("formSelectIncidencias").style.display = "none";
   document.getElementById("formInsertIncidencias").style.display = "none";
   document.getElementById("formUpdateIncidencias").style.display = "block";
   document.getElementById("formDeleteIncidencias").style.display = "none";
}
function main_showFormDeleteIncidencias(){
   document.getElementById("formSelectIncidencias").style.display = "none";
   document.getElementById("formInsertIncidencias").style.display = "none";
   document.getElementById("formUpdateIncidencias").style.display = "none";
   document.getElementById("formDeleteIncidencias").style.display = "block";
}

// Funciones para capa Zonasmetro
function main_showDivZonasmetro(){
   document.getElementById("sectionPlacas").style.display = "none";
   document.getElementById("sectionIncidencias").style.display = "none";
   document.getElementById("sectionZonasmetro").style.display = "block";
}
function main_showFormSelectZonasmetro(){
   document.getElementById("formSelectZonasmetro").style.display = "block";
   document.getElementById("formInsertZonasmetro").style.display = "none";
   document.getElementById("formUpdateZonasmetro").style.display = "none";
   document.getElementById("formDeleteZonasmetro").style.display = "none";
}
function main_showFormInsertZonasmetro(){
   document.getElementById("formSelectZonasmetro").style.display = "none";
   document.getElementById("formInsertZonasmetro").style.display = "block";
   document.getElementById("formUpdateZonasmetro").style.display = "none";
   document.getElementById("formDeleteZonasmetro").style.display = "none";
}
function main_showFormUpdateZonasmetro(){
   document.getElementById("formSelectZonasmetro").style.display = "none";
   document.getElementById("formInsertZonasmetro").style.display = "none";
   document.getElementById("formUpdateZonasmetro").style.display = "block";
   document.getElementById("formDeleteZonasmetro").style.display = "none";
}
function main_showFormDeleteZonasmetro(){
   document.getElementById("formSelectZonasmetro").style.display = "none";
   document.getElementById("formInsertZonasmetro").style.display = "none";
   document.getElementById("formUpdateZonasmetro").style.display = "none";
   document.getElementById("formDeleteZonasmetro").style.display = "block";
}

function main_hide(){
    //document.getElementById("sectionPlacas").style.display = "none";
    //document.getElementById("formSelectPlacas").style.display = "none";
    //document.getElementById("formInsertPlacas").style.display = "none";
    //document.getElementById("formUpdatePlacas").style.display = "none";
    //document.getElementById("formDeletePlacas").style.display = "none";
    document.getElementById("sectionIncidencias").style.display = "none";
    document.getElementById("sectionPlacas").style.display = "none";
    //document.getElementById("formSelectIncidencias").style.display = "none";
    //document.getElementById("formInsertIncidencias").style.display = "none";
    //document.getElementById("formUpdateIncidencias").style.display = "none";
    //document.getElementById("formDeleteIncidencias").style.display = "none";
    //document.getElementById("formSelectPlacas").style.display = "none";
    //document.getElementById("formInsertPlacas").style.display = "none";
    //document.getElementById("formUpdatePlacas").style.display = "none";
    //document.getElementById("formDeletePlacas").style.display = "none";
    //document.getElementById("sectionZonasmetro").style.display = "none";
    //document.getElementById("formSelectZonasmetro").style.display = "none";
    //document.getElementById("formInsertZonasmetro").style.display = "none";
    //document.getElementById("formUpdateZonasmetro").style.display = "none";
    //document.getElementById("formDeleteZonasmetro").style.display = "none";
}

function main_init(){
    // main_hide();
	//document.getElementById("buttonShowDivPlacas").addEventListener("click", main_showDivPlacas);
	//document.getElementById("buttonShowDivIncidencias").addEventListener("click", main_showDivIncidencias);
	//document.getElementById("buttonShowDivZonasmetro").addEventListener("click", main_showDivZonasmetro);
	// Funciones para botones de Placas
	//document.getElementById("buttonSelectPlacas").addEventListener("click", main_showFormSelectPlacas);
	//document.getElementById("buttonInsertPlacas").addEventListener("click", main_showFormInsertPlacas);
	//document.getElementById("buttonUpdatePlacas").addEventListener("click", main_showFormUpdatePlacas);
	//document.getElementById("buttonDeletePlacas").addEventListener("click", main_showFormDeletePlacas);
	   // Funciones para botones de Incidencias
    //document.getElementById("buttonSelectIncidencias").addEventListener("click", main_showFormSelectIncidencias);
    //document.getElementById("buttonInsertIncidencias").addEventListener("click", main_showFormInsertIncidencias);
    //document.getElementById("buttonUpdateIncidencias").addEventListener("click", main_showFormUpdateIncidencias);
    //document.getElementById("buttonDeleteIncidencias").addEventListener("click", main_showFormDeleteIncidencias);
        // Funciones para botones de Zonasmetro
    //document.getElementById("buttonSelectZonasmetro").addEventListener("click", main_showFormSelectZonasmetro);
    //document.getElementById("buttonInsertZonasmetro").addEventListener("click", main_showFormInsertZonasmetro);
    //document.getElementById("buttonUpdateZonasmetro").addEventListener("click", main_showFormUpdateZonasmetro);
    //document.getElementById("buttonDeleteZonasmetro").addEventListener("click", main_showFormDeleteZonasmetro);

}

window.onload = function() {
	main_init();
};

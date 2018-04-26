/*class confusion {
    constructor() {
        for i 
    }
}*/

$( document ).ready(function() {


    // Variables GLOBALES
    var matUser = [];
    var html = "";
    var sommeNonTrouvekVoisin = 0;
    var sommeTrouvekVoisin = 0;
    var removedClass = '';
    var addedClass = '';
    // Permet de savoir si l'utilisateur a envoyé une correction ou non.
    var correctionOrNot = 0;

    for(var i = 0;i<10;i++)
    {
	    html += "<tr>";
	    for(var j = 0;j<10;j++)
	    {		
	        if(i == j){
	            html += '<td class=\"diago\"></td>';
	        }else if((i == (j-1)) || (i == (j+1))){
		        html += '<td class=\"proche\"></td>';
	        }else{
	            html += '<td class=\"loin\"></td>';
	        }
	    }
	    html += "</tr>";
    }
    $("#matrix1").html(html);
    $("#matrix2").html(html);
    $("#matrix3").html(html);
    
    initConfusion();
    
    function initConfusion(){
        $("#matrix1 td").each(function(index) {
            $(this).text(0); 
        });
        
        $("#matrix2 td").each(function(index) {
            $(this).text(0); 
        });
        
        $("#matrix3 td").each(function(index) {
            $(this).text(0); 
        });
    }

    // Permet de remplir le tableau avec la matrice remplit par l'utilisateur
    function remplitTableau(){
        $("#draw td" ).each(function( index ) {
	        if($(this).hasClass('white'))
	        {		
		        matUser[index]=  -1;
	        }	
	        else
	        {		
		        matUser[index] = +1;		
	        }
        });
    }
    
    $("#draw td").mousedown(function() {
        if($(this).hasClass('white')){
            removedClass = 'white';
            addedClass = 'black';
        }else {
            removedClass = 'black';
            addedClass = 'white';
        }
        $(this).removeClass(removedClass);
	    $(this).addClass(addedClass);
        $("#draw td").bind('mouseover',function(){
	        $(this).removeClass(removedClass);
	        $(this).addClass(addedClass);	
        });
    });
    $(document).mouseup(function() {
        $("#draw td").unbind('mouseover');
    });

    $("#reset").click(function() {	   
        // Remise à zero des valeurs
        $("#correct_input").val('');
        
        $("#draw td").each(function( index ) {
	        if($(this).hasClass('black'))
	        {		
		        $(this).removeClass('black');
		        $(this).addClass('white');	
		        matUser[index] = -1;
	        }		
        });
    });
    

    $("#send").click(function() {	   
        // On assume que lorsque une réponse est bonne de la part des algos, on ne fournit pas de correction : 
        // Il faut donc mettre la matrice de confusion à jour
        if(correctionOrNot == 1){
            miseAJourConfusion($('#resultVoisin').val());
        }
        correctionOrNot = 1;
        
        // Remplit matUser
        remplitTableau(); 
        if(isEmpty(matUser)){
            alert("Je ne peux pas envoyer un truc vide !!");
            return;
        } 
        
        // Remise à zero des valeurs
        $('#resultVoisin').val('');
        $('#resultBayes').val('');
        $('#resultRN').val('');
        $("#correct_input").val('');
        
        $.ajax({
            type: "POST",
            url:'/benchmark',
            data: JSON.stringify(matUser),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                $('#resultVoisin').val(data.kVoisin);
                $('#resultBayes').val(data.bayes);
                $('#resultRN').val(data.RN);
            },
            failure: function(errMsg) {
                alert("Le serveur a rencontré un problème.");
            }
        });
    });
    
    $("#correct").click(function() {
        if(typeof matUser == 'undefined' || matUser.lenght == 0){
            alert("Je ne peux pas corriger quelque chose que vous n'avez pas envoyé");
        }
        var dataToSend = {};
        var correctValue = $("#correct_input").val();
        
        // Construction de la réponse, en forme de JSON correspondant à une ligne de la base de donnée
        dataToSend.value = correctValue;
        dataToSend.data = matUser;
        
        $.ajax({
            type: "POST",
            url:'/correction',
            data: JSON.stringify(dataToSend),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(){
                $("#correct_input").empty();
            },
            failure: function(errMsg) {
                alert(errMsg);
            }   
        });
        
        miseAJourConfusion(correctValue);
        correctionOrNot = 0;
    });
    
    function miseAJourConfusion(expertValue){
        
        var resultkVoisin = $('#resultVoisin').val();
        var resultBayes = $('#resultBayes').val();
        var resultRN = $('#resultRN').val();
        
        var valuekVoisin = (10*expertValue) + parseInt(resultkVoisin);
        var valueBayes = (10*expertValue) + parseInt(resultBayes);
        var valueRN = (10*expertValue) + parseInt(resultRN);
        var sommeTrouve = 0;
        var sommeTotale = 0;
        var pourcent = 0;
        
        // Parcours de la matrice 10x10, mise à jour de la matrice de confusion
        $("#matrix1 td").each(function (index) {
                        
            indexConfusionMAJ(index, valuekVoisin, $(this));      
            // Calcul du pourcentage de reussite
            if (index%11 == 0){
                sommeTrouve += parseInt($(this).text());
            }
            sommeTotale += parseInt($(this).text());
        });
  
        // Mise à jour pourcentage confusion pour kVoisin
        pourcent = parseInt((sommeTrouve/sommeTotale) * 100);
        $("#spankVoisin").html(pourcent);
        sommeTrouve = 0;
        sommeTotale = 0;

        $("#matrix2 td").each(function (index) {
            // Calcul du pourcentage de reussite
            indexConfusionMAJ(index, valueBayes, $(this));      

            if (index%11 == 0){
                sommeTrouve += parseInt($(this).text());
            }
            sommeTotale += parseInt($(this).text());
        });
        // Mise à jour pourcentage confusion pour Baye
        pourcent = parseInt((sommeTrouve/sommeTotale) * 100);
        $("#spanBaye").html(pourcent);
        sommeTrouve = 0;
        sommeTotale = 0;

        $("#matrix3 td").each(function (index) {
            indexConfusionMAJ(index, valueRN, $(this));      
            // Calcul du pourcentage de reussite
            if (index%11 == 0){
                sommeTrouve += parseInt($(this).text());
            }
            sommeTotale += parseInt($(this).text());
        });
        // Mise à jour pourcentage confusion pour Reseau de Neurone
        pourcent = parseInt((sommeTrouve/sommeTotale) * 100);
        $("#spanRN").html(pourcent);
    }
    
    function indexConfusionMAJ(index, value, obj){
        if(index == value){
            var chiffre = obj.text();
            obj.text(parseInt(chiffre)+1);
            return 0;
        }else return 1;       
    }
    
    function isEmpty(matrice){
        for (var i = 0; i < matrice.length; i++){
            if (matrice[i] == 1){
                return false;
            }
        }
        return true;
    }
});


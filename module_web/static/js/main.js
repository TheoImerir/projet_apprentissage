/*class confusion {
    constructor() {
        for i 
    }
}*/

$( document ).ready(function() {


    // Variables GLOBALES
    var matUser = [];
    var html = "";

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
    
    $("#draw td").click(function() {	
        if($(this).hasClass('white'))
        {
	        $(this).removeClass('white');
	        $(this).addClass('black');
        }
        else{
	        $(this).removeClass('black');
	        $(this).addClass('white');	
        }
    });

    $("#reset").click(function() {	
    
        // Remise à zero des valeurs
        $('#resultVoisin').val('');
        $('#resultBayes').val('');
        $('#resultRN').val('');
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
     
        remplitTableau();  
        // Remise à zero des valeurs
        $('#resultVoisin').val('');
        $('#resultBayes').val('');
        $('#resultRN').val('');
        $("#correct_input").val('');
        
        $.ajax({
                type: "POST",
                url:'http://localhost:5000/benchmark',
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
        var dataToSend = {};
        var correctValue = $("#correct_input").val();
        
        // Construction de la réponse, en forme de JSON correspondant à une ligne de la base de donnée
        dataToSend.value = correctValue;
        dataToSend.data = matUser;
        
        $.ajax({
            type: "POST",
            url:'http://localhost:5000/correction',
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
    });
    
    function miseAJourConfusion(expertValue){
        
        var resultkVoisin = $('#resultVoisin').val();
        var resultBayes = $('#resultBayes').val();
        var resultRN = $('#resultRN').val();
        
        var valuekVoisin = (10*expertValue) + parseInt(resultkVoisin);
        var valueBayes = (10*expertValue) + parseInt(resultBayes);
        var valueRN = (10*expertValue) + parseInt(resultRN);
        
        // Parcours de la matrice 10x10, mise à jour de la matrice de confusion
        $("#matrix1 td").each(function (index) {
            if(indexConfusionMAJ(index, valuekVoisin, $(this)) == 0){
                return;
            }
        });
        
        $("#matrix2 td").each(function (index) {
            if(indexConfusionMAJ(index, valueBayes, $(this)) == 0){
                return;
            }
        });        
        
        $("#matrix3 td").each(function (index) {
            if(indexConfusionMAJ(index, valueRN, $(this)) == 0){
                return;
            }
        });
    }
    
    function indexConfusionMAJ(index, value, obj){
        if(index == value){
            var chiffre = obj.text();
            obj.text(parseInt(chiffre)+1);
            return 0;
        }else return 1;       
    }
});


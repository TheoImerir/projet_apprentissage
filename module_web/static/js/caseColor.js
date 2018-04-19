

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
$("#draw td").each(function( index ) {
	if($(this).hasClass('black'))
	{		
		$(this).removeClass('black');
		$(this).addClass('white');	
		monTableau[index] = -1;
	}		
});
});
var monTableau = [];
$("#send").click(function() {	
$("#draw td" ).each(function( index ) {
	if($(this).hasClass('white'))
	{		
		monTableau[index]=  -1;
	}	
	else
	{		
		monTableau[index] = +1;		
	}	
});



$.ajax({
        type: "POST",
        url:'http://172.30.0.71:5000/test',
        data: JSON.stringify(monTableau),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(data){alert(data);},
        failure: function(errMsg) {
            alert(errMsg);
        }
  });
});


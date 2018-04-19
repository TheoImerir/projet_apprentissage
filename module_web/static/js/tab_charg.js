var html = "";

for(var i = 0;i<10;i++)
{
	html += "<tr>";
	for(var j = 0;j<10;j++)
	{			
		html += '<td></td>';
	}
	html += "</tr>";
	
}
$("#matrix1").html(html);
$("#matrix2").html(html);
$("#matrix3").html(html);

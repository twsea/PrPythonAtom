function create () 
{
    var el = document.createElement("p");        
    var text = document.createTextNode("Запрос на сервер отправлен, ожидайте ответ...");       
    el.appendChild(text);                                
    document.body.appendChild(el);  
}

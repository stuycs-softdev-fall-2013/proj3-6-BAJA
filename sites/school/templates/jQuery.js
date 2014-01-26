var todolist = document.getElementById("todo");
var todoitem = document.createElement("li");
todoitem.appendChild(document.createTextNode("Final Grade: 65"));
todoitem.addEventListener("click",function() {
    todolist.removeChild(this)} );
todolist.appendChild(todoitem);


var main = function(){
    var todolist = document.getElementById("todo");
    
    var removeFromList = function(){
    todolist.removeChild(this);
    }
    
    var moveToTODO = function(){
    var textbox = document.getElementById("inputGrade");
    var input = textbox.value;
    var todoitem = document.createElement("li");
    todoitem.appendChild(document.createTextNode(input));
    todoitem.addEventListener("click",removeFromList);
    todolist.appendChild(todoitem);
    textbox.value = "";
    }
    
    var submitbutton = document.getElementById("submit");
    submitbutton.addEventListener("click",moveToTODO);
}();

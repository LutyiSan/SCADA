


function elemDisplay(open,close, form){
let openElem = document.querySelector(open);
let closeElem  = document.querySelector(close);
let formElem = document.querySelector(form);
openElem.addEventListener("click", function(){

formElem.style.display = 'block';
});
closeElem.addEventListener("click", function(){
formElem.style.display = 'none';
});
};

function elemClose(close, form){
let closeElem  = document.querySelector(close);
let formElem = document.querySelector(form);
closeElem.addEventListener("click", function(){
formElem.style.display = 'none';
});
};

function elemOpen(close, form){
let closeElem  = document.querySelector(close);
let formElem = document.querySelector(form);
closeElem.addEventListener("click", function(){
formElem.style.display = 'block';
});
};

function resetForm(command,form){
let elem = document.querySelector(form);
let action = document.querySelector(command);
console.log(elem);
console.log(action);
action.addEventListener("click", function(){
elem.reset();
});
};



function typeTag(element, click){
let elem = document.querySelector(element);
let cl = document.querySelector(click);
cl.addEventListener('click', function(){
    if (elem.value === 'modbus'){
        document.querySelector('#modbus-tag').style.display = 'block';
        document.querySelector('#type-tag').style.display = 'none';
        }
    else if (elem.value === 'bacnet'){
        document.querySelector('#bacnet-tag').style.display = 'block';
        document.querySelector('#type-tag').style.display = 'none';
        }
});
};



window.onload = function () {
elemDisplay("#new-project", "#close-save-project","#save-project");
elemDisplay("#new-device", "#close-save-device","#save-device");
elemDisplay("#new-tags", "#close-type-tag","#type-tag");
typeTag('#sel-tag', '#save-type-tag')
elemClose("#close-type-tag","#type-tag");
elemClose("#close-bacnet-tag","#bacnet-tag");
elemClose("#close-modbus-tag","#modbus-tag");
resetForm("#next-device", "#save-device");
resetForm("#next-bacnet-tag", "#bacnet-tag");
resetForm("#next-modbus-tag", "#modbus-tag");











}
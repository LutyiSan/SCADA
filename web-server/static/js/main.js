

function formDisplay(open,close, form){
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

function typeTag(element, click){
let elem = document.querySelector(element);
let cl = document.querySelector(click);
cl.addEventListener('click', function(){
    if (elem.name == 'modbus'){
        document.querySelector('#modbus-tag').style.display = 'block';
        document.querySelector('#type-tag').style.display = 'none';
        }
    else{
        document.querySelector('#bacnet-tag').style.display = 'block';
        document.querySelector('#type-tag').style.display = 'none';
        }
});
};



window.onload = function () {
formDisplay("#new-project", "#close-save-project","#save-project");
formDisplay("#new-device", "#close-save-device","#save-device");
formDisplay("#new-tags", "#close-type-tag","#type-tag");
typeTag('#sel-tag', '#save-type-tag')
formDisplay("#tags", "#close-type-tag","#type-tag");
}
/* addLoadEvent 
   fonction pour unobtrusive dhtml
   thanks to Simon Willison for this */

function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}

/* getElementsByTagNames
   récupère dans un tableau les elts correspondant à une *liste* de tags
   classés par ordre d'apparition dans le document
   thanks to Peter Paul Koch for this */

function getElementsByTagNames(list,obj) {
	if (!obj) var obj = document;
	var tagNames = list.split(',');
	var resultArray = new Array();
	for (var i=0;i<tagNames.length;i++) {
		var tags = obj.getElementsByTagName(tagNames[i]);
		for (var j=0;j<tags.length;j++) {
			resultArray.push(tags[j]);
		}
	}
	var testNode = resultArray[0];
	if (!testNode) return [];
	if (testNode.sourceIndex) {
		resultArray.sort(function (a,b) {
				return a.sourceIndex - b.sourceIndex;
		});
	}
	else if (testNode.compareDocumentPosition) {
		resultArray.sort(function (a,b) {
				return 3 - (a.compareDocumentPosition(b) & 6);
		});
	}
	return resultArray;
}

function addOpenCloseTitles() {
	var h4title = getElementsByTagNames('h4,h5');
	//var h4title = document.getElementsByTagName('h4');
	for (var i=0; i < h4title.length; i++) {
		/* Le nextSibling n'est pas la div mais un noeud texte vide dans Firefox, mais pas dans IE */
		var suivant = h4title[i].nextSibling;
		while (suivant.nodeName != 'DIV') { suivant = suivant.nextSibling; }
		var divId = suivant.id;
		//alert(divId);
		if (divId) {
			var a = document.createElement('a');
			a.href = 'javascript:openClose(\''+divId+'\',0)';
			var noeudTexte = h4title[i].firstChild;
			a.appendChild(document.createTextNode(noeudTexte.nodeValue));
			//a.appendChild(document.createTextNode(' [open/close]'));
			//a.style.fontSize = 'x-small';
			//a.style.fontWeight = 'normal';
			a.style.textDecoration = 'none';
			a.style.position = 'static';
			//a.style.color = '#000';
			h4title[i].removeChild(noeudTexte);
			h4title[i].appendChild(a);

		}
	}
}

function openCloseAll() {
	js_flag = -js_flag;
	mOpenClose(js_fermer, js_flag);
	/*mOpenClose(js_ouvrir, js_flag);*/
}

function addOpenCloseAll() {
	var h3title = document.getElementsByTagName('h3');
	if (h3title[0]) {
		var a = document.createElement('a');
		a.href = 'javascript:openCloseAll()';
		var noeudTexte = h3title[0].firstChild;
		a.appendChild(document.createTextNode(noeudTexte.nodeValue));
		a.style.textDecoration = 'none';
		h3title[0].removeChild(noeudTexte);
		h3title[0].appendChild(a);
	}
}

function addHelp() {
	var theDivs = document.getElementsByTagName('div');
	for (var i=0; i < theDivs.length; i++) {
		if (theDivs[i].className == 'chapter') {
			var chapDiv = theDivs[i];
			break;
		}
	}
	var theHelp = document.createElement('p');
	var hideHelp = document.createElement('a');
	theHelp.id = 'aide';
	theHelp.className = 'nop';
	var leTexte, cacheLe;
	switch (chapDiv.lang) {
		case 'fr':
		leTexte = "Cliquer sur les titres des sections pour cacher ou montrer leur contenu. ";
		leTexte += "Cliquer sur le titre du chapitre pour cacher ou montrer l'ensemble du cours. ";
		cacheLe = "Cacher l'aide";
		break;
		default:
		leTexte = "Click on the sections (sub)titles to show or hide their contents. ";
		leTexte += "Click on the chapter's title to show or hide everything. ";
		cacheLe = "Hide this"
	}
	theHelp.appendChild(document.createTextNode(leTexte));
	hideHelp.appendChild(document.createTextNode(cacheLe));
	hideHelp.href = 'javascript: openClose(\'aide\',0)';
	theHelp.appendChild(hideHelp);
	chapDiv.parentNode.insertBefore(theHelp,chapDiv);
}

function findStructure() {
	var theDivs = document.getElementsByTagName('div');
	for (var i=0; i < theDivs.length; i++) {
		if (theDivs[i].className == 'section') {
			if (theDivs[i+1].className == 'subsection') {
				js_ouvrir.push(theDivs[i].id); 
			} else { 
				js_fermer.push(theDivs[i].id); 
			}
		} else if (theDivs[i].className == 'subsection') {
			js_fermer.push(theDivs[i].id);
		}
	} 
	mOpenClose(js_fermer,1);
	mOpenClose(js_ouvrir,1);
}

function addHelpButton() {
	var taskBar = document.getElementById('taskbar');
	var b = document.createElement('p');
	b.className = 'aide';
	var a = document.createElement('a');
	a.href = 'javascript:openClose(\'aide\',0)';
	a.appendChild(document.createTextNode('?'));
	b.appendChild(a);
	taskBar.insertBefore(b, taskBar.firstChild);
}

function openClose(id,mode)
{
    if(document.getElementById) {
        element = document.getElementById(id);
    } else return;
    
    if(element.style) {
        if(mode == 0) {
            if(element.style.display == 'block' ) {
                element.style.display = 'none';
            } else {
                element.style.display = 'block';
            }
        } else if(mode == 1) {
            element.style.display = 'block';
        } else if(mode == -1) {
            element.style.display = 'none';
        }
    }
}

function mOpenClose(idArray,mode)
{
    for(var i=0;i<idArray.length;i++) {
        openClose(idArray[i],mode);
    }
}


var js_ouvrir = new Array();
var js_fermer = new Array();
var js_flag = 1;

addLoadEvent( function() {
/*	addHelp(); */
	openClose('aide',1);
	findStructure();
	addOpenCloseTitles();
	addOpenCloseAll();
/*	addHelpButton(); */
});


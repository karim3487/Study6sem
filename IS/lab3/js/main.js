Array.prototype.contains = function(object) {
	for(i = 0; i < this.length; i++){
		if(this[i] == object){
			return i;
		}
	}
	return -1;
};

Array.prototype.add = function(object) {
	if(object === null && this.contains(object) >= 0){
		return false;
	}
	else{
		this[this.length] = object;
		return true;
	}
};

Array.prototype.remove = function(from, to) {
	var rest = this.slice((to || from) + 1 || this.length);
	this.length = from < 0 ? this.length + from : from;
	return this.push.apply(this, rest);
};

Array.prototype.isEmpty = function() {
	if(this == null || this.length == 0){
		return true;
	}
	else{
		return false;
	}
};

function isInCircle(x, y, center_x, center_y, radius) {
	return (Math.pow(x-center_x, 2) + Math.pow(y - center_y, 2) < radius*radius)
}

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}


var sequence = 0;
var root;
var nodes = new Array();
var canvas;
var context;
var surface;
// var divOpcoes;
var divOpcoesAberta = false;
var clickLiberado = false;

var execucao = new Array();
var focoExecucao = new Array();

function init() {
	// cria tela
	surface = new Tela(1000, 600);

	// cria nodo raiz
	root = new Nodo();
	root.x = (surface.largura - larguraNodo) / 2;
	root.y = 50;
	root.nivel = 0;
	root.y = root.nivel * (alturaNodo + espacoNivel) + 50;

	// adiciona raiz à lista de nodos
	nodes.add(root);
	
	divOpcoes = document.createElement('div');
	divOpcoes.id = "divOpcoes";

	// sei la o q ... canvas
	canvas = document.getElementById('drawing');
	context = canvas.getContext('2d');
	
	canvas.addEventListener('mousedown', ckmouse, false);

	// desenha a tela
	surface.draw();
}

function ckmouse(e) {
	
	$(divOpcoes).hide();

	var nodo = null;
	for (var i = 0; i < nodes.length; i++) {
		if (isInCircle(e.offsetX, e.offsetY, nodes[i].x, nodes[i].y, larguraNodo / 2)) {
			//alert(e.offsetX + " | " + e.offsetY);
			nodo = nodes[i];
			break;
		}
	}
	
	if (nodo == null) {
		return;
	}
	
	divOpcoes.innerHTML = "";
	
	var div = document.createElement('div');
	div.innerHTML = "Добавить дочерний узел";
	$(div).bind('click', function(){
		$(divOpcoes).hide();
		adicionarFilho(nodo.pk);
	});
	$(divOpcoes).append(div);
	
	if (nodo.filhos.isEmpty()) {
		div = document.createElement('div');
		div.innerHTML = "Изменить значение";
		$(div).bind('click', function(){
			$(divOpcoes).hide();
			editar(nodo.pk);
		});
		$(divOpcoes).append(div);
	}
	
	if (nodo.pk != root.pk) {
		div = document.createElement('div');
		div.innerHTML = "Удалить узел";
		$(div).bind('click', function(){
			$(divOpcoes).hide();
			excluirNodo(nodo.pk, true);
		});
		$(divOpcoes).append(div);
	}
		
	$("#main").append(divOpcoes);
	$(divOpcoes).css('position', 'absolute');
	$(divOpcoes).css('left', e.offsetX + 'px');
	$(divOpcoes).css('top', e.offsetY + 'px');
	$(divOpcoes).show();
	
}

function Nodo() {
	this.pk;
	this.valor = null;
	this.quebra = false;
	this.pai = null;
	this.filhos = new Array();

	this.x;
	this.y;
	this.nivel;

	this.draw = drawNodo;

	obterPK(this);
}

function obterPK(objeto) {
	objeto.pk = ++sequence;
}

function findByPK(pk) {
	for (var i = 0; i < nodes.length; i++) {
		if (nodes[i].pk == pk) {
			return nodes[i];
		}
	}
	return null;
}

function adicionarFilho(pkPai) {
	var pai = findByPK(pkPai);
	if (pai == null) {
		// TODO erro
		alert("Erro");
		return false;
	}
	var nodo = new Nodo();
	nodo.pai = pai;
	pai.filhos.add(nodo);
	nodes.add(nodo);
	nodo.nivel = pai.nivel + 1;
	nodo.y = nodo.nivel * (alturaNodo + espacoNivel) + 50;
	pai.valor = null;

	var t = document.getElementById('drawing')
	var height = t.height;
	var temp = nodo.y;
	if (nodo.nivel > 7) {
		if ((temp+50) > height) {
			t.height = temp+50;
			surface.altura = temp+50;
		}
	}

	surface.draw();
}

function reorganiza(nodo) {
	if (nodo.pk != root.pk) {
		pai = nodo.pai;
		// se for filho unico, x = x do pai
		if (pai.filhos.length == 1) {
			nodo.x = pai.x;
		} else {

			var posInicial = 0;
			var quant = pai.filhos.length;
			var larg = (pai.x + larguraNodo/2) * 2;

			// se não for raiz
			if (pai.pk != 1) {
				var paiCalculo = pai;
				while (paiCalculo.pai.filhos.length < 2 && paiCalculo.pai.pai != null) {
					paiCalculo = paiCalculo.pai;
				}
				
				var pos = paiCalculo.pai.filhos.contains(paiCalculo);
				if (pos == 0) {
					if (paiCalculo.pai.filhos.length > 1) {
						var paiAnt = paiCalculo.pai.filhos[pos+1];
						larg = paiAnt.x - paiCalculo.x;
						posInicial = paiCalculo.x - larg/2 + larguraNodo;
						larg -= larguraNodo;
					}
				} else {
					var paiAnt = paiCalculo.pai.filhos[pos-1];
					larg = paiCalculo.x - paiAnt.x;
					posInicial = larg/2 + larguraNodo + paiAnt.x;
					larg -= larguraNodo;
				}
			}

			var largNodo = larg/quant; // se menor q 50, n deixa add
			var nodoX = largNodo/2 - larguraNodo/2;
			var acum = posInicial;
			for (var i = 0; i < quant; i++) {
				pai.filhos[i].x = acum + nodoX;
				acum += largNodo;
			}
		}
	}
	
	if (!nodo.filhos.isEmpty()) {
		for (var i = 0; i < nodo.filhos.length; i++) {
			reorganiza(nodo.filhos[i]);
		}
	}
}

function calculoPosPai(nivelAtual) {
	// varre todos os nodos
	for (var i = 0; i < nodes.length; i++) {
		var nodo = nodes[i];
		// se nivel certo e 'x' ainda não definido
		if (nodo.nivel == nivelAtual - 1 && nodo.x == null) {
			var quantFilhos = nodo.filhos.length;
			var menorX = nodo.filhos[0].x;
			var maiorX = nodo.filhos[quantFilhos-1].x;

			nodo.x = (menorX + maiorX) / 2;
		}
	}
}

function reposicionaFolhas(nodo, folhaAtual, larguraPorNodo) {
	if (nodo.filhos.isEmpty()) {
		nodo.x = folhaAtual * larguraPorNodo + larguraPorNodo / 2;
		folhaAtual++;
	} else {
		for (var i = 0; i < nodo.filhos.length; i++) {
			folhaAtual = reposicionaFolhas(nodo.filhos[i], folhaAtual, larguraPorNodo);
		}
	}

	return folhaAtual;
}

function reorganizaNew() {
	// limpa o x de todos os nodos
	for (var i = 0; i < nodes.length; i++) {
		nodes[i].x = null;
	}

	// obtem quantidade de folhas e maior nivel
	var quantFolhas = 0;
	var maiorNivel = 0;
	for (var i = 0; i < nodes.length; i++) {
		var nodo = nodes[i];
		if (nodo.filhos.isEmpty()) {
			quantFolhas++;
			if (nodo.nivel > maiorNivel) {
				maiorNivel = nodo.nivel;
			}
		}
	}

	// calcula largura disponível para cada folha
	var larguraPorNodo = surface.largura / quantFolhas;

	// coloca as folhas no lugar
	reposicionaFolhas(root, 0, larguraPorNodo);

	nivelAtual = maiorNivel;
	while (nivelAtual > 0) {
		calculoPosPai(nivelAtual);
		nivelAtual--;
	}
}

function editar (pkNodo) {
	var nodo = findByPK(pkNodo);
	if (nodo == null) {
		alert("Узла не существует");
		return false;
	}
	var valor = prompt("Введите число:");
	
	if (!isNumber(valor)) {
		alert("Это не число.");
		return;
	}
	nodo.valor = valor;
	
	surface.draw();
}

function folhasPreenchidas() {
	for (var i = 0; i < nodes.length; i++) {
		var nodo = nodes[i];
		if (nodo.filhos.isEmpty() && nodo.valor == null) {
			alert("Вы должны установить значение для всех конечных узлов.");
			return false;
		}
	}
	return true;
}

function excluirNodo(pkNodo, alertar) {
	if (pkNodo == 1) {
		alert("Вы не можете удалить корневой узел.")
		return;
	}

	var nodo = findByPK(pkNodo);
	if (nodo == null) {
		alert("Узла не существует");
		return false;
	}
	
	if (!nodo.filhos.isEmpty()) {
		var resposta = true;
		if (alertar) {
			resposta = confirm("У этого узла есть дети. Вы хотите убить его детей? :'(");
		}
		if (resposta) {
			while (nodo.filhos.length > 0) {
				excluirNodo(nodo.filhos[0].pk, false);
			}
			//for (var i = 0; i < nodo.filhos.length; i++) {
				
			//}
		} else {
			return;
		}
	}

	if (nodo.pai != null) {
		var pos = nodo.pai.filhos.contains(nodo);
		nodo.pai.filhos.remove(pos);
	}

	var pos = nodes.contains(nodo);
	nodes.remove(pos);

	if (alertar) {
		surface.draw();
	}
}

var execucaoPassoAtual = 0;
function executarPassoAnterior() {
	if (execucaoPassoAtual > 0) {
		execucaoPassoAtual--;
	}
	surface.draw(execucao[execucaoPassoAtual]);
	focoExecucao[execucaoPassoAtual].draw("red");
}

function executarProximoPasso() {
	if (execucaoPassoAtual < execucao.length - 1) {
		execucaoPassoAtual++;
	}
	surface.draw(execucao[execucaoPassoAtual]);
	focoExecucao[execucaoPassoAtual].draw("red");
}

function executarFinal() {
	surface.draw();
}

function finalizarExecucao() {
	surface.draw();

	execucaoPassoAtual = 0;
	execucao = new Array();
	focoExecucao = new Array();

	$("#menu_execucao").hide();
	$("#menu_principal").show();
}

function limpaValoresEQuebras() {
	for (var i = 0; i < nodes.length; i++) {
		nodes[i].quebra = false;
		if (!nodes[i].filhos.isEmpty()) {
			nodes[i].valor = null;
		}
	}

	surface.draw();
}

function clonaNodo(nodo, newPai) {
	var n = new Nodo();
	//n.pk = nodo.pk;
	n.valor = nodo.valor;
	n.quebra = nodo.quebra;
	n.pai = newPai;
	n.filhos = new Array();
	for (var i = 0; i < nodo.filhos.length; i++) {
		n.filhos.add(nodo.filhos[i]);
	}

	n.x = nodo.x;
	n.y = nodo.y;
	n.nivel = nodo.nivel;

	return n;
}

function clonaRecursivo(nodo, estado, nodoAtual) {
	if (nodo.filhos.isEmpty()) {
		return;
	} else {
		for (var i = 0; i < nodo.filhos.length; i++) {
			var novoNodo = clonaNodo(nodo.filhos[i], nodo);
			estado.add(novoNodo);
			clonaRecursivo(novoNodo, estado, nodoAtual);

			if (nodoAtual == nodo.filhos[i]) {
				focoExecucao.add(novoNodo);
			}

			nodo.filhos[i] = novoNodo;
		}
	}
}

function getEstadoAtual(nodoAtual) {
	var newRaiz = clonaNodo(root, null);

	var estAtual = new Array();
	estAtual.add(newRaiz);

	if (nodoAtual == root) {
		focoExecucao.add(newRaiz);
	}

	clonaRecursivo(newRaiz, estAtual, nodoAtual);

	return estAtual;
}

function criaMiniMax() {
	if (folhasPreenchidas()){
		limpaValoresEQuebras();
		execucao = new Array();
		focoExecucao = new Array();
		execucaoPassoAtual = 0;
		minimax(root);
		$("#menu_execucao").show();
		$("#menu_principal").hide();
	}
}

function minimax(nodo) {
	execucao.add(getEstadoAtual(nodo));

	if (!nodo.filhos.isEmpty()){
		for (var i = 0; i < nodo.filhos.length; i++) {
			console.log("nodo => " + nodo.filhos[i].pk);
			minimax(nodo.filhos[i]);
		}
	}
	if (nodo == root) {
		return;
	}
	if (nodo.pai.valor == null) {
		nodo.pai.valor = nodo.valor;
	} else {
		var max = false;
		if (nodo.nivel%2 == 0){
			max = true;
		}
		var valorNodo = Math.floor(nodo.valor);
		var valorPai = Math.floor(nodo.pai.valor);
		if (max) {
			if(valorNodo < valorPai){
				nodo.pai.valor = nodo.valor;
			}
		} else {
			if(valorNodo > valorPai){
				nodo.pai.valor = nodo.valor;
			}
		}
	}
	execucao.add(getEstadoAtual(nodo));
	focoExecucao[focoExecucao.length-1] = focoExecucao[focoExecucao.length-1].pai;
}

function criaPoda() {
	if (folhasPreenchidas()){
		limpaValoresEQuebras();
		execucao = new Array();
		focoExecucao = new Array();
		execucaoPassoAtual = 0;
		poda(root);
		$("#menu_execucao").show();
		$("#menu_principal").hide();
	}
}

function poda(nodo) {
	execucao.add(getEstadoAtual(nodo));
	if (!nodo.filhos.isEmpty()){
		var quebra = false;
		for (var i = 0; i < nodo.filhos.length; i++) {
			console.log("nodo => " + nodo.filhos[i].pk);

			if (!quebra) {
				quebra = poda(nodo.filhos[i]);
			} else {
				nodo.filhos[i].quebra = true;
			}
		}
	}
	if (nodo == root) {
		return false;
	}

	var max = false;
	if (nodo.nivel%2 == 0){
		max = true;
	}

	if (nodo.pai.valor == null) {
		nodo.pai.valor = nodo.valor;
	} else {
		var valorNodo = Math.floor(nodo.valor);
		var valorPai = Math.floor(nodo.pai.valor);
		if (max) {
			if(valorNodo < valorPai){
				nodo.pai.valor = nodo.valor;
			}
		} else {
			if(valorNodo > valorPai){
				nodo.pai.valor = nodo.valor;
			}
		}
	}
	execucao.add(getEstadoAtual(nodo));
	focoExecucao[focoExecucao.length-1] = focoExecucao[focoExecucao.length-1].pai;

	return testaPodaPai(nodo, max);
}

function testaPodaPai(nodo, max) {

	if (nodo.pai == null) {
		return;
	}

	var valor = nodo.pai.valor;
	var quebra = false;

	var nodoAux = nodo.pai.pai;
	while (nodoAux != null) {
		if ((nodoAux.nivel%2 == 0) == max) {
			if (nodoAux.valor != null) {
				if (max) {
					if (Math.floor(valor) <= Math.floor(nodoAux.valor)) {
						quebra = true;
						break;
					}
				} else {
					if (Math.floor(valor) >= Math.floor(nodoAux.valor)) {
						quebra = true;
						break;
					}
				}
			}
		}
		nodoAux = nodoAux.pai;
	}

	if (quebra) {
		console.log(nodo.valor + " | " + nodo.nivel);
		return true;
	}

	return false;
}

function Tela(largura, altura) {
	this.largura = largura;
	this.altura = altura;

	this.draw = drawTela;
}

function drawTela(nodoList) {
	if (!nodoList) {
		nodoList = nodes;
	}

	reorganizaNew(root);

	context.beginPath();

	context.fillStyle = "white";
	context.fillRect(0, 0, this.largura, this.altura);
	context.closePath();

	maxNivel = 0;
	for (var i = 0; i < nodoList.length; i++) {
		if (nodoList[i].nivel > maxNivel) {
			maxNivel = nodoList[i].nivel;
		}
	}

			
	for(var i = 0; i < nodoList.length; i++){
		if (nodoList[i].pai != null) {
			context.beginPath();
			context.strokeStyle = "black";
			context.moveTo(nodoList[i].x, nodoList[i].y);
			context.lineTo(nodoList[i].pai.x, nodoList[i].pai.y);
			context.stroke();
			context.closePath();

			// se nodo possui quebra, desenha o X
			if (nodoList[i].quebra) {
				context.beginPath();
				context.strokeStyle = "red";
				var centroX = (Math.floor(nodoList[i].x) + Math.floor(nodoList[i].pai.x)) / 2;
				var centroY = (Math.floor(nodoList[i].y) + Math.floor(nodoList[i].pai.y)) / 2
				context.moveTo(centroX-10, centroY-10);
				context.lineTo(centroX+10, centroY+10);

				context.moveTo(centroX-10, centroY+10);
				context.lineTo(centroX+10, centroY-10);
				context.stroke();
				context.closePath();
			}
			
			//context.moveTo(nodoList[i].x + larguraNodo/2,100);
			//context.lineTo(200,200);
		}
	}
	
	for(var i = 0; i < nodoList.length; i++){
		nodoList[i].draw();
	}


	for (var i = 0; i <= maxNivel; i++) {
		context.fillStyle = "rgba(200,200,200, 0.4)";
		context.strokeStyle = "rgba(200,200,200, 0.4);"
		context.font = "bold 22px 'Arial'";
		
		var str = new String(this.valor);
		
		context.fillText((i%2 ? "MIN" : "MAX"), 30, (espacoNivel+alturaNodo) + i*(espacoNivel+alturaNodo) - 17);
		context.fillText((i%2 ? " MIN" : "MAX"), 926, (espacoNivel+alturaNodo) + i*(espacoNivel+alturaNodo) - 17);
		
		context.moveTo(30, (espacoNivel+alturaNodo) + i*(espacoNivel+alturaNodo) + 15);
		context.lineTo(970, (espacoNivel+alturaNodo) + i*(espacoNivel+alturaNodo) + 15);
		context.stroke();

	}
}

function drawNodo(color) {
	if (!color) {
		color = "black"
		fillstyle = "white";
		firstfill = "rgb(160,160,160)";
	} else {
		fillstyle = "rgb(240,240,240)";
		firstfill = color;
	}
	context.fillStyle = firstfill;
	context.strokeStyle = color;
	var y = this.nivel * (alturaNodo + espacoNivel) + 50;
	context.beginPath();
	context.arc(this.x, this.y, alturaNodo/2+2, 0, 2 * Math.PI, false);
	context.fill();
	context.closePath();
	
	context.fillStyle = fillstyle;
	context.beginPath();
	//context.strokeRect(this.x, y, larguraNodo, alturaNodo);
	context.arc(this.x, this.y, alturaNodo/2, 0, 2 * Math.PI, false);
	context.stroke();
	context.fill();
	context.closePath();
	
	if (this.valor != null) {
		context.fillStyle = "blue";
		context.font = "bold 13px 'Courier New'";
		
		var str = new String(this.valor);
		var pxLetra = 8;
		var larg = pxLetra * str.length;
		
		context.fillText(this.valor, this.x - larg/2, this.y + 4);
	}
}

function excluirTudo() {
	limpaValoresEQuebras();
	nodes.remove(1, nodes.length-1);
	nodes[0].x = (surface.largura - larguraNodo) / 2;
	nodes[0].valor = null;
	nodes[0].filhos = new Array();
	sequence = 1;
	var execucao = new Array();
	var focoExecucao = new Array();
	execucaoPassoAtual = 0;
	$("#menu_principal").show();
	$("#menu_execucao").hide();
	surface.draw();
}

$("document").ready(function(){

	init();

	$("button").button();

    $(document).keydown(function(e){
    	var key = e.which;
    	if ($("#menu_execucao").css('display') != "none") {
	    	if (key == 37) {
	    		executarPassoAnterior();
	    	} else if (key == 39) {
	    		executarProximoPasso();
	    	}
	    }
    });

});

function gerarExemplo() {
	excluirTudo();

	adicionarFilho(1);
	adicionarFilho(1);

	adicionarFilho(2);
	adicionarFilho(2);
	adicionarFilho(3);
	adicionarFilho(3);

	adicionarFilho(4);
	adicionarFilho(4);
	adicionarFilho(5);
	adicionarFilho(5);
	adicionarFilho(6);
	adicionarFilho(6);
	adicionarFilho(7);
	adicionarFilho(7);

	adicionarFilho(8);
	adicionarFilho(8);
	adicionarFilho(9);
	adicionarFilho(9);
	adicionarFilho(10);
	adicionarFilho(10);
	adicionarFilho(11);
	adicionarFilho(11);
	adicionarFilho(12);
	adicionarFilho(12);
	adicionarFilho(13);
	adicionarFilho(13);
	adicionarFilho(14);
	adicionarFilho(14);
	adicionarFilho(15);
	adicionarFilho(15);


	nodes[15].valor = 8;
	nodes[16].valor = 23;
	nodes[17].valor = -47;
	nodes[18].valor = 28;
	nodes[19].valor = -30;
	nodes[20].valor = -37;
	nodes[21].valor = 3;
	nodes[22].valor = -41;
	nodes[23].valor = -19;
	nodes[24].valor = 4;
	nodes[25].valor = -49;
	nodes[26].valor = 4;
	nodes[27].valor = 43;
	nodes[28].valor = 45;
	nodes[29].valor = -26;
	nodes[30].valor = -14;

	surface.draw();
}


var larguraNodo = 25;
var alturaNodo = 25;
var espacoNivel = 50
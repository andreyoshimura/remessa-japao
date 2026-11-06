// Parceiros com versão própria das ferramentas (?p=código). Lista única para todas as páginas.
// Só códigos desta lista mudam o topo; qualquer outro mostra a versão normal do Radar Nihon.
// Foto só com autorização (arquivo em parceiros/). Para tirar a marca de alguém: apagar a linha.
window.RN_PARCEIROS = {
  carla: {
    nome: "Carla no Japão", iniciais: "CS", foto: "parceiros/carla.jpg", ref: "carla-no-japao",
    canal: "https://www.youtube.com/@soucarlasantana",
    visto: { url: "https://www.youtube.com/watch?v=-F1g4Aie5nQ", txt: "Assista ao vídeo da Carla: como renovar o cartão de residência" },
    conversor: { url: "https://www.youtube.com/@soucarlasantana", txt: "Assista aos vídeos da Carla sobre a vida no Japão" }
  }
};
window.RN_parceiro = function(){
  var k = (new URLSearchParams(location.search).get("p") || "").toLowerCase();
  var L = window.RN_PARCEIROS;
  return Object.prototype.hasOwnProperty.call(L, k) ? { k: k, d: L[k] } : null;
};
window.RN_selo = function(P){
  var av = P.d.foto ? '<img src="' + P.d.foto + '" alt="">' : '<span>' + P.d.iniciais + '</span>';
  return '<a class="parceiro" href="' + P.d.canal + '" target="_blank" rel="noopener"><span class="pav">' + av + '</span>' +
         '<span class="ptx"><b>__TITULO__ ' + P.d.nome + '</b><small>feito com Radar Nihon</small></span></a>';
};

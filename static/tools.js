const tools = [ 
  {
    icon: "fas fa-file-word",
    title: "Word para PDF",
    description: "Converta seus arquivos .docx para PDF mantendo a formatação original.",
    link: "/wordpdf",
    category: "pdf"
  },
  {
    icon: "fas fa-file-pdf",
    title: "PDF para Word",
    description: "Transforme arquivos PDF em documentos editáveis no formato Word (.docx).",
    link: "/pdfword",
    category: "pdf"
  },
  {
    icon: "fas fa-image",
    title: "PNG para PDF",
    description: "Converta imagens PNG em arquivos PDF de forma simples e rápida.",
    link: "/imgpdf",
    category: "pdf"
  },
  {
    icon: "fas fa-file-image",
    title: "PDF para PNG",
    description: "Extraia imagens PNG a partir das páginas de um arquivo PDF.",
    link: "/pdfimg",
    category: "pdf"
  },
  {
    icon: "fas fa-file-pdf",
    title: "Juntar PDFs",
    description: "Junte seus arquivos PDF em um único documento de forma fácil.",
    link: "/juntarpdf",
    category: "pdf"
  },
  {
    icon: "fa-regular fa-file-lines",
    title: "Conversor Texto",
    description: "Converter de maiúscula para minúscula ou aplicar outros formatos com um clique.",
    link: "/textconverter",
    category: "texto"
  },
  {
    icon: "fas fa-compress",
    title: "Comprimir PDF",
    description: "Reduza o tamanho do seu arquivo PDF mantendo a qualidade.",
    link: "/compress",
    category: "pdf"
  },
  {
    icon: "fas fa-file-archive",
    title: "Descompactar ZIP",
    description: "Envie um arquivo ZIP e descompacte seu conteúdo rapidamente.",
    link: "/decompress",
    category: "outros"
  }
];

const toolGrid = document.getElementById("toolGrid");
const searchInput = document.getElementById("searchInput");
const clearSearch = document.getElementById("clearSearch");
const filterBtns = document.querySelectorAll(".filter-btn");
function renderTools(filter = "all", searchTerm = "") {
  toolGrid.innerHTML = "";

  const filtered = tools.filter(tool => {
    const matchCategory = filter === "all" || tool.category === filter;
    const matchSearch = tool.title.toLowerCase().includes(searchTerm.toLowerCase());
    return matchCategory && matchSearch;
  });

if (filtered.length === 0) {
  toolGrid.innerHTML = `
    <div class="not-found">
      <img src="/static/editorinho1.png" alt="Nenhum resultado">
      <h3>Ops! Nada foi encontrado...</h3>
      <p>Tente outra palavra-chave ou selecione uma categoria diferente.</p>
    </div>
  `;
  return;
}
  filtered.forEach(tool => {
    const card = document.createElement("div");
    card.className = "tool-card";
    card.innerHTML = `
      <div class="tool-icon"><i class="${tool.icon}"></i></div>
      <h2>${tool.title}</h2>
      <p>${tool.description}</p>
      <a href="${tool.link}" class="btn">Converter</a>
    `;
    toolGrid.appendChild(card);
  });
}
searchInput.addEventListener("input", () => {
  clearSearch.style.display = searchInput.value ? "inline" : "none";
  const activeFilter = document.querySelector(".filter-btn.active").dataset.filter;
  renderTools(activeFilter, searchInput.value);
});
clearSearch.addEventListener("click", () => {
  searchInput.value = "";
  clearSearch.style.display = "none";
  const activeFilter = document.querySelector(".filter-btn.active").dataset.filter;
  renderTools(activeFilter, "");
});
filterBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    filterBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    renderTools(btn.dataset.filter, searchInput.value);
  });
});
renderTools();

/*
  1) Carrega a lista de produtos da API (GET)
*/
const getList = () => {
  fetch("http://127.0.0.1:5000/produtos")
    .then(r => {
      if (!r.ok) throw new Error("Falha ao carregar lista");
      return r.json();
    })
    .then(data => {
      data.produtos.forEach(p =>
        insertList(p.nome, p.urgencia, p.data)
      );
    })
    .catch(err => console.error("Erro ao obter lista:", err));
};
getList();

/*
  2) Envia um novo produto para a API (POST) — como JSON e retorna Promise
*/
const postItem = (nome, urgencia, data) => {
  const payload = {
    nome: nome,
    urgencia: urgencia,
    data: data
  };

  console.log("Enviando payload:", payload);

  return fetch("http://127.0.0.1:5000/produto", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  })
    .then(r => {
      if (!r.ok) {
        if (r.status === 409) {
          throw new Error("Produto já existe! Escolha outro nome.");
        }
        throw new Error("Erro ao salvar produto");
      }
      return r.json();
    });
};

/*
  3) Deleta produto (DELETE)
*/
const deleteItem = nome => {
  fetch("http://127.0.0.1:5000/produto?nome=" + encodeURIComponent(nome), {
    method: "DELETE"
  })
    .then(r => {
      if (!r.ok) {
        throw new Error("Erro ao deletar produto");
      }
      return r.json();
    })
    .catch(err => console.error("Erro ao deletar:", err));
};

/*
  4) Função chamada ao clicar no botão "Adicionar"
     Garante que a data seja formatada corretamente para o backend
*/
function newItem() {
  const nome     = document.getElementById("newInput").value.trim();
  const urgencia = document.getElementById("newUrgency").value.trim();
  const dataInput = document.getElementById("newData").value;

  if (!nome) {
    alert("⚠️ Escreva o nome do item.");
    return;
  }
  if (!urgencia) {
    alert("⚠️ Selecione a urgência.");
    return;
  }
  if (!dataInput) {
    alert("⚠️ Informe a data.");
    return;
  }

  // Monta data ISO para satisfazer o Pydantic (datetime)
  const dataISO = dataInput + "T00:00:00";

  postItem(nome, urgencia, dataISO)
    .then(() => {
      insertList(nome, urgencia, dataInput); // Mostra só a data no HTML
      document.getElementById("newInput").value = "";
      document.getElementById("newUrgency").value = "";
      document.getElementById("newData").value = "";
    })
    .catch(err => alert("❌ " + err.message));
}

/*
  5) Insere item na tabela
*/
function insertList(nome, urgencia, data) {
  const table = document.getElementById("myTable");
  const row = table.insertRow();
  [nome, urgencia, data].forEach(text => {
    const cell = row.insertCell();
    cell.textContent = text;
  });
  insertDeleteButton(row.insertCell());
  attachDeleteEvents();
}

function insertDeleteButton(cell) {
  const span = document.createElement("span");
  span.textContent = "×";
  span.className = "close";
  cell.appendChild(span);
}

function attachDeleteEvents() {
  document.querySelectorAll(".close").forEach(btn => {
    btn.onclick = () => {
      const row = btn.parentElement.parentElement;
      const nome = row.cells[0].innerText;
      if (confirm("Você tem certeza?")) {
        row.remove();
        deleteItem(nome);
      }
    };
  });
}

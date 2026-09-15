const btn_submit = document.querySelector("#btn_submit");

btn_submit.addEventListener("click", async (event) => {
  const input = document.querySelector("#csvFile");

  if (!input.files[0]) {
    console.error("Nenhum arquivo selecionado");
    return;
  }

  const file = input.files[0];

  const formData = new FormData();

  formData.append("file", file);

  try {
    const condicao = "producao";
    let url = "";

    if (condicao == "local") {
      url = "http://127.0.0.1:8000/convert/";
    } else {
      url = "https://conversor-csv.onrender.com/convert/";
    }

    const resposta = await fetch(url, {
      method: "POST",
      body: formData,
    });

    const resposta_json = await resposta.json();

    MontarTabela(resposta_json);
  } catch (erro) {
    console.error(erro);
  }
});

function MontarTabela(res) {
  const tbody = document.querySelector("#tabela tbody");
  const valor_total = document.querySelector("#valor_total");

  let total = 0;

  tbody.innerHTML = "";

  res.forEach((ocorrencia) => {
    const row = document.createElement("tr");

    total += ocorrencia.valor_informado;

    row.innerHTML = `
            <td>${ocorrencia.prestador}</td>
            <td>${ocorrencia.data}</td>
            <td>${ocorrencia.uf}</td>
            <td>${ocorrencia.servico}</td>
            <td>${ocorrencia.resultado}</td>
            <td>${ocorrencia.rastreado}</td>
            <td>${ocorrencia.houve_guincho}</td>
            <td>${ocorrencia.tipo_veiculo}</td>
            <td>${ocorrencia.placa}</td>
            <td>${ocorrencia.chassi}</td>
            <td>${ocorrencia.qtd_agente}</td>
            <td>${ocorrencia.horas_extra}</td>
            <td>${ocorrencia.valor_guincho}</td>
            <td>${ocorrencia.valor_informado}</td>
          `;

    tbody.appendChild(row);
  });

  valor_total.value = `R$${total}`;

  BaixarCsv(res);
}

function BaixarCsv(res) {
  const csv = Papa.unparse(res);

  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const urllink = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = urllink;
  link.download = "Ocorrencias_Aguia_Suhai.csv";

  link.click();

  URL.revokeObjectURL(urllink);
}

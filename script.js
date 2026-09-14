const btn_submit = document.querySelector("#btn_submit");

btn_submit.addEventListener("click", async (event) => {
  const input = document.querySelector("#csvFile");
  const tbody = document.querySelector("#tabela tbody");
  const valor_total = document.querySelector("#valor_total");

  let total = 0;

  if (!input.files[0]) {
    alert("Nenhum arquivo selecionado");
    event.preventDefault();
    return;
  }

  const file = input.files[0];

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,

    complete: async (resultado) => {
      try {
        const ocorrencias = resultado.data;

        const resposta = await fetch("http://127.0.0.1:8000/convert/", {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(ocorrencias),
        });

        if (!resposta.ok) {
          throw new Error(`HTTP error! status: ${resposta.status}`);
        }

        const resposta_json = await resposta.json();

        tbody.innerHTML = "";

        resposta_json.forEach((ocorrencia) => {
          const row = document.createElement("tr");

          total += ocorrencia.valor_informado;

          row.innerHTML = `
            <td>${ocorrencia.Prestador}</td>
            <td>${ocorrencia.Data}</td>
            <td>${ocorrencia.UF}</td>
            <td>${ocorrencia.Serviço}</td>
            <td>${ocorrencia.Resultado}</td>
            <td>${ocorrencia.Rastreado}</td>
            <td>${ocorrencia["Houve Guincho"]}</td>
            <td>${ocorrencia.tipo_veiculo}</td>
            <td>${ocorrencia.Placa}</td>
            <td>${ocorrencia.chassi}</td>
            <td>${ocorrencia["Qtd Agente"]}</td>
            <td>${ocorrencia["Horas Extra (Qnt horas)"]}</td>
            <td>${new Intl.NumberFormat("pt-BR", {
              style: "currency",
              currency: "BRL",
            }).format(ocorrencia["Valor Guincho"])}</td>
            <td>${new Intl.NumberFormat("pt-BR", {
              style: "currency",
              currency: "BRL",
            }).format(ocorrencia.valor_informado)}</td>
          `;

          tbody.appendChild(row);
        });

        valor_total.value = `R$${total}`;

        const csv = Papa.unparse(resposta_json);

        const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.download = "Ocorrencias_Aguia_Suhai.csv";

        link.click();

        URL.revokeObjectURL(url);
      } catch (erro) {
        console.error(erro);
        alert("Erro ao enviar o arquivo.");
      }
    },
  });
});

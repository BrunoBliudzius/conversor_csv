from fastapi import APIRouter, UploadFile, File
from typing import Annotated
import csv
import io

router = APIRouter()


@router.post("/")
async def convert_csv(file: Annotated[UploadFile, File()]):
    arquivo = io.TextIOWrapper(file.file, encoding="utf-8")

    leitor = csv.DictReader(arquivo)

    ocorrencias = list(leitor)

    ocorrencias_formatas = []

    for ocorrencia in ocorrencias:

        data = ocorrencia.get("DATA", "").strip()
        regiao = ocorrencia.get("REGIÃO", "").strip()
        localizado = ocorrencia.get("LOCALIZADO", "").strip()
        qru = ocorrencia.get("QRU", "").strip()
        picape = ocorrencia.get("PICAPE", "").strip()
        placa = ocorrencia.get("PLACA", "").strip()
        qtd_agente = int(ocorrencia.get("N° DE AGENTES", "").strip() or 0)
        valor_horas_extra = ocorrencia.get("HORA EXTRA", "").strip()

        if regiao in ["NORTE", "LESTE", "SUL", "OESTE"]:
            uf = f"São Paulo - Zona {regiao.title()}"
        elif regiao == "INTERIOR":
            uf = "São Paulo - Interior"
        elif regiao == "LITORAL":
            uf = "São Paulo - Litoral"
        else:
            uf = regiao

        if localizado == "Recuperado":
            servico = "Recuperação"
        elif localizado == "Acionamento":
            servico = "Acionamento"
        else:
            servico = "Projeto DP"

        if servico in ["Recuperação", "Projeto DP"]:
            resultado = "Recuperado"
        else:
            resultado = "Perdido"

        if qru in ["ROUBO", "FURTO"]:
            rastreado = "SIM"
        else:
            rastreado = "NÃO"

        if picape == "SIM":
            houve_guincho = "SIM"
        else:
            houve_guincho = "NÃO"

        valor_guincho = 100 if houve_guincho == "SIM" else 0

        horas_extra = (
            int(
                float(
                    valor_horas_extra.replace("R$", "")
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                )
            )
            if valor_horas_extra
            else 0
        )

        if servico == "Projeto DP":
            valor_agente = 315

        elif uf == "São Paulo - Interior":
            valor_agente = 390 if resultado == "Recuperado" else 160

        elif uf == "São Paulo - Litoral":
            valor_agente = 370 if resultado == "Recuperado" else 160

        elif uf in [
            "São Paulo - Zona Norte",
            "São Paulo - Zona Leste",
            "São Paulo - Zona Oeste",
            "São Paulo - Zona Sul",
        ]:
            valor_agente = 365 if resultado == "Recuperado" else 125

        else:
            valor_agente = 630 if resultado == "Recuperado" else 420

        valor_informado = (valor_agente * qtd_agente) + horas_extra + valor_guincho

        resposta = {
            "prestador": "Aguia Recuperações",
            "data": data,
            "uf": uf,
            "servico": servico,
            "resultado": resultado,
            "rastreado": rastreado,
            "houve_guincho": houve_guincho,
            "tipo_veiculo": "...",
            "placa": placa,
            "chassi": "...",
            "qtd_agente": qtd_agente,
            "horas_extra": horas_extra,
            "valor_guincho": valor_guincho,
            "valor_informado": valor_informado,
        }

        ocorrencias_formatas.append(resposta)

    return ocorrencias_formatas

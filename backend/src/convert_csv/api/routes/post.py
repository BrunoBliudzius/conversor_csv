from fastapi import APIRouter, Body
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter()


class Ocorrencia(BaseModel):
    data: str = Field(alias="DATA")
    qru: str = Field(alias="QRU")
    regiao: str = Field(alias="REGIÃO")
    placa: str = Field(alias="PLACA")
    veiculo: str = Field(alias="VEÍCULO")
    localizado: str = Field(alias="LOCALIZADO")
    numero_agentes: str = Field(alias="N° DE AGENTES")
    picape: str = Field(alias="PICAPE")
    hora_extra: str = Field(alias="HORA EXTRA")


class OcorrenciaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    Prestador: str = "Aguia Recuperações"
    data: str = Field(alias="Data")
    uf: str = Field(alias="UF")
    servico: str = Field(alias="Serviço")
    resultado: str = Field(alias="Resultado")
    rastreado: str = Field(alias="Rastreado")
    houve_guincho: str = Field(alias="Houve Guincho")
    tipo_veiculo: str = "..."
    placa: str = Field(alias="Placa")
    chassi: str = "..."
    qtd_agente: int = Field(alias="Qtd Agente")
    horas_extra: int = Field(alias="Horas Extra (Qnt horas)")
    valor_guincho: int = Field(alias="Valor Guincho")
    valor_informado: int


@router.post("/", response_model=list[OcorrenciaResponse])
async def post_csv(ocorrencias: Annotated[list[Ocorrencia], Body()]):
    respostas: list[OcorrenciaResponse] = []

    for ocorrencia in ocorrencias:
        data = ocorrencia.data.strip()

        regiao = ocorrencia.regiao.strip()

        if regiao in ["NORTE", "LESTE", "SUL", "OESTE"]:
            uf = f"São Paulo - Zona {regiao.title()}"
        elif regiao == "INTERIOR":
            uf = "São Paulo - Interior"
        elif regiao == "LITORAL":
            uf = "São Paulo - Litoral"
        else:
            uf = regiao

        if ocorrencia.localizado == "Recuperado":
            servico = "Recuperação"
        elif ocorrencia.localizado == "Acionamento":
            servico = "Acionamento"
        else:
            servico = "Projeto DP"

        if servico == "Recuperação" or servico == "Projeto DP":
            resultado = "Recuperado"
        else:
            resultado = "Perdido"

        if ocorrencia.qru == "ROUBO" or ocorrencia.qru == "FURTO":
            rastreado = "SIM"
        else:
            rastreado = "NÃO"

        if ocorrencia.picape == "SIM":
            houve_guincho = "SIM"
        else:
            houve_guincho = "NÃO"

        placa = ocorrencia.placa.strip()

        qtd_agente = int(ocorrencia.numero_agentes.strip() or 0)

        valor_horas_extra = ocorrencia.hora_extra.strip()
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

        valor_guincho = 100 if houve_guincho == "SIM" else 0

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

        resposta = OcorrenciaResponse(
            data=data,
            uf=uf,
            servico=servico,
            resultado=resultado,
            rastreado=rastreado,
            houve_guincho=houve_guincho,
            placa=placa,
            qtd_agente=qtd_agente, 
            horas_extra=horas_extra,
            valor_guincho=valor_guincho,
            valor_informado=valor_informado,
        )

        respostas.append(resposta)

    return respostas

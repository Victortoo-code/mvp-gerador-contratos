import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import base64
import os

# Título
st.title("Gerador de Contratos - MVP")
st.write("Preencha os dados abaixo para gerar o contrato em PDF com cláusulas e timbre pré-definidos.")

# Formulário de entrada
with st.form("formulario_contrato"):
    nome_contratante = st.text_input("Nome do contratante")
    cpf_contratante = st.text_input("CPF do contratante")
    endereco_contratante = st.text_input("Endereço do contratante")
    servico = st.text_input("Serviço contratado")
    valor = st.text_input("Valor do contrato")
    data_contrato = st.date_input("Data do contrato", value=datetime.today())
    enviar = st.form_submit_button("Gerar contrato")

# Processar
if enviar:
    # Carregar modelo
    modelo = DocxTemplate("contrato_modelo.docx")

    # Contexto para preenchimento
    contexto = {
        "nome_contratante": nome_contratante,
        "cpf_contratante": cpf_contratante,
        "endereco_contratante": endereco_contratante,
        "servico": servico,
        "valor": valor,
        "data_contrato": data_contrato.strftime("%d/%m/%Y")
    }

    # Preencher e salvar
    modelo.render(contexto)
    caminho_saida = "contrato_preenchido.docx"
    modelo.save(caminho_saida)

    # Converter para PDF
    try:
        from docx2pdf import convert
        convert(caminho_saida, "contrato_preenchido.pdf")
        with open("contrato_preenchido.pdf", "rb") as f:
            pdf = f.read()
        b64 = base64.b64encode(pdf).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="contrato.pdf">📄 Baixar contrato em PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
    except:
        st.error("Erro na conversão para PDF. Baixe o DOCX abaixo.")
        with open(caminho_saida, "rb") as f:
            docx = f.read()
        b64 = base64.b64encode(docx).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="contrato.docx">📄 Baixar contrato em Word</a>'
        st.markdown(href, unsafe_allow_html=True)

    # Limpeza
    os.remove(caminho_saida)
    if os.path.exists("contrato_preenchido.pdf"):
        os.remove("contrato_preenchido.pdf")

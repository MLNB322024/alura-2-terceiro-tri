```python
import gradio as gr
import hashlib
import string

# =========================================
# SENTINEL SECURITY - CONFIGURACOES
# =========================================

LETRAS = "abcdefghijklmnopqrstuvwxyz"
LETRAS_CODIFICADAS = "phqgiumeaylnofdxjkrcvstzwb"

NUMEROS = "0123456789"
NUMEROS_CODIFICADOS = "8642097531"


# =========================================
# MODULO DE CODIFICACAO
# =========================================

def converter_mensagem(mensagem, decodificar=False):
    if not mensagem:
        return "Nenhuma mensagem foi informada."

    origem_letras = LETRAS
    destino_letras = LETRAS_CODIFICADAS
    origem_numeros = NUMEROS
    destino_numeros = NUMEROS_CODIFICADOS

    if decodificar:
        origem_letras, destino_letras = (
            destino_letras, origem_letras
        )
        origem_numeros, destino_numeros = (
            destino_numeros, origem_numeros
        )

    mapa = str.maketrans(
        origem_letras + origem_letras.upper() + origem_numeros,
        destino_letras + destino_letras.upper() + destino_numeros
    )

    return mensagem.translate(mapa)


# =========================================
# MODULO DE HASH
# =========================================

def calcular_assinatura(texto):
    if not texto:
        return "Insira um texto para continuar."

    digest = hashlib.sha256(
        texto.encode("utf-8")
    ).hexdigest()

    return (
        f"ALGORITMO: SHA-256\n"
        f"ASSINATURA: {digest}\n"
        f"TAMANHO DO TEXTO: {len(texto)} caracteres"
    )


# =========================================
# MODULO DE SEGURANCA DE SENHAS
# =========================================

def analisar_credencial(senha):
    if not senha:
        return "Nenhuma senha foi inserida."

    testes = {
        "Pelo menos 8 caracteres": len(senha) >= 8,
        "Pelo menos 12 caracteres": len(senha) >= 12,
        "Letras minusculas": any(c.islower() for c in senha),
        "Letras maiusculas": any(c.isupper() for c in senha),
        "Numeros": any(c.isdigit() for c in senha),
        "Simbolos": any(c in string.punctuation for c in senha)
    }

    total = sum(testes.values())

    if len(senha) < 8:
        nivel = "BAIXO"
    elif total >= 5:
        nivel = "ALTO"
    elif total >= 3:
        nivel = "MEDIO"
    else:
        nivel = "BAIXO"

    checklist = "\n".join(
        f"[{'X' if valido else ' '}] {criterio}"
        for criterio, valido in testes.items()
    )

    return (
        f"INDICE DE SEGURANCA: {nivel}\n"
        f"CRITERIOS CUMPRIDOS: {total}/6\n\n"
        f"{checklist}"
    )


# =========================================
# INTERFACE SENTINEL
# =========================================

with gr.Blocks(
    theme=gr.themes.Glass(
        primary_hue="indigo",
        secondary_hue="slate"
    ),
    title="Sentinel Security"
) as painel:

    gr.Markdown("""
    # SENTINEL SECURITY
    ### Painel de ferramentas digitais
    ---

    Centralize operacoes de codificacao, verificacao
    de integridade e avaliacao de credenciais.
    """)

    with gr.Tab("Painel inicial"):
        gr.Markdown("""
        ## Central de operacoes

        Selecione uma das ferramentas disponiveis:

        - **Codificacao:** transforma letras e numeros.
        - **Decodificacao:** recupera o conteudo original.
        - **Integridade:** calcula uma assinatura SHA-256.
        - **Credenciais:** verifica criterios basicos de senhas.
        """)

    with gr.Tab("Codificacao"):
        gr.Markdown("### Conversor de mensagens")

        entrada_cod = gr.Textbox(
            label="Conteudo de entrada",
            placeholder="Digite sua mensagem...",
            lines=4
        )

        botao_cod = gr.Button(
            "INICIAR CODIFICACAO",
            variant="primary"
        )

        saida_cod = gr.Textbox(
            label="Resultado da operacao",
            lines=4
        )

        botao_cod.click(
            lambda texto: converter_mensagem(texto),
            inputs=entrada_cod,
            outputs=saida_cod
        )

    with gr.Tab("Decodificacao"):
        gr.Markdown("### Recuperacao de mensagens")

        entrada_decod = gr.Textbox(
            label="Conteudo recebido",
            placeholder="Cole o texto codificado...",
            lines=4
        )

        botao_decod = gr.Button(
            "REVERTER CODIFICACAO",
            variant="primary"
        )

        saida_decod = gr.Textbox(
            label="Conteudo recuperado",
            lines=4
        )

        botao_decod.click(
            lambda texto: converter_mensagem(
                texto, decodificar=True
            ),
            inputs=entrada_decod,
            outputs=saida_decod
        )

    with gr.Tab("Integridade"):
        gr.Markdown("### Gerador de assinatura digital SHA-256")

        entrada_hash = gr.Textbox(
            label="Texto a ser analisado",
            lines=3
        )

        botao_hash = gr.Button(
            "CALCULAR ASSINATURA",
            variant="primary"
        )

        saida_hash = gr.Textbox(
            label="Relatorio de integridade",
            lines=4
        )

        botao_hash.click(
            calcular_assinatura,
            inputs=entrada_hash,
            outputs=saida_hash
        )

    with gr.Tab("Credenciais"):
        gr.Markdown("### Avaliador de senhas")

        entrada_senha = gr.Textbox(
            label="Credencial para verificacao",
            placeholder="Digite uma senha...",
            type="password"
        )

        botao_senha = gr.Button(
            "EXECUTAR ANALISE",
            variant="primary"
        )

        saida_senha = gr.Textbox(
            label="Relatorio de seguranca",
            lines=9
        )

        botao_senha.click(
            analisar_credencial,
            inputs=entrada_senha,
            outputs=saida_senha
        )

    gr.Markdown("""
    ---
    **SENTINEL SECURITY** | Ambiente educacional de seguranca digital
    """)


if __name__ == "__main__":
    painel.launch()
```

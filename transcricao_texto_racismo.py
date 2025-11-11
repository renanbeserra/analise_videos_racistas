import time
import google.generativeai as genai

# Configure sua chave da API
genai.configure(api_key="CHAVE_DA_SUA_API_AQUI")
model = genai.GenerativeModel("gemini-2.5-pro")

def analisar_conteudo_racista(texto):
    prompt = """
    Analise o texto fornecido e identifique se há conteúdo racista. 
    Considere:
    1. Palavras ou expressões discriminatórias
    2. Estereótipos raciais
    3. Preconceitos implícitos ou explícitos
    4. Discurso de ódio racial
    
    Forneça uma análise objetiva com:
    - Identificação de trechos problemáticos (se houver)
    - Explicação do por que são considerados racistas
    - Nível de gravidade (baixo, médio, alto)
    - Recomendações para tornar o discurso mais inclusivo
    
    Se não houver conteúdo racista, indique isso claramente.
    """
    
    response = model.generate_content([
        prompt,
        texto
    ])
    
    return response.text

def processar_video(caminho_video):
    # Faz upload do vídeo
    uploaded_file = genai.upload_file(caminho_video)

    # Espera até o arquivo ser processado
    while uploaded_file.state.name == "PROCESSING":
        time.sleep(5)
        uploaded_file = genai.get_file(uploaded_file.name)

    if uploaded_file.state.name != "ACTIVE":
        raise Exception(f"Falha ao processar arquivo: {uploaded_file.state.name}")

    # Gera a transcrição completa
    response = model.generate_content([
        uploaded_file,
        "Transcreva integralmente o áudio deste vídeo em português, sem resumir, mantendo a pontuação e falas separadas."
    ])
    
    transcricao = response.text
    analise = analisar_conteudo_racista(transcricao)
    
    return transcricao, analise

if __name__ == "__main__":
    # Exemplo de uso direto do script
    caminho_video = "caminho/para/seu/video.mp4"
    transcricao, analise = processar_video(caminho_video)
    print("\nTRANSCRIÇÃO COMPLETA:\n")
    print(transcricao)
    print("\nANALISANDO CONTEÚDO QUANTO A EXPRESSÕES RACISTAS...\n")
    print(analise)
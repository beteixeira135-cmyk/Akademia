"""Contagem de tokens. Usa o tiktoken (o200k_base, padrão dos modelos GPT-4o em diante) se estiver instalado e com a
codificação disponível; senão, estima por caracteres (≈ 3,6 caracteres por token em português, aproximação declarada).
A contagem exata para o Claude exige a API count_tokens da Anthropic (POST /v1/messages/count_tokens, com chave)."""
_ENC = None


def contar(texto: str) -> tuple[int, str]:
    global _ENC
    if _ENC is None:
        try:
            import tiktoken
            _ENC = tiktoken.get_encoding("o200k_base")
        except Exception:
            _ENC = False
    if _ENC:
        return len(_ENC.encode(texto)), "tiktoken o200k_base"
    return round(len(texto) / 3.6), "estimativa (caracteres ÷ 3,6)"

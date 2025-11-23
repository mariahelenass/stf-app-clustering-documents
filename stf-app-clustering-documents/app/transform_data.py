import unicodedata
import re
import spacy
import os
from nltk.corpus import stopwords


# "stopwords" brasileiras
with open("stopwords_br.txt", "r", encoding="utf-8") as f:
    stop_words = set([x.strip().lower() for x in f.readlines()])

# "stopwords" jurídicas
with open("stopwords_juridicas.txt", "r", encoding="utf-8") as f:
    juridicas = set([x.strip().lower() for x in f.readlines()])

# estados brasileiros e topicos comuns
with open("topicos_comuns.txt", "r", encoding="utf-8") as f:
    topicos_comuns = set([x.strip().lower() for x in f.readlines()])

stop_words = stop_words.union(juridicas)


def remove_accents(text: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(c)
    )


def normalize_spacing(text: str) -> str:
    invisible = [
        "\u00A0", "\u2000", "\u2001", "\u2002", "\u2003",
        "\u2004", "\u2005", "\u2006", "\u2007", "\u2008",
        "\u2009", "\u200A", "\u202F", "\u205F", "\u3000",
        "\u200B"    
    ]
    for sp in invisible:
        text = text.replace(sp, " ")

    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_citations(text: str) -> str:
    text = re.sub(r"\bart\.?\s*(\d+)\b", r"art_\1", text)
    text = re.sub(r"§\s*(\d+)", r"par_\1", text)

    roman_map = {
        "i":1, "ii":2, "iii":3, "iv":4, "v":5, "vi":6,
        "vii":7, "viii":8, "ix":9, "x":10, "xi":11, "xii":12
    }

    def roman_to_num(m):
        r = m.group(1).lower()
        return f"inc_{roman_map.get(r, r)}"

    text = re.sub(r"\binciso\s+([ivx]+)\b", roman_to_num, text)
    return text


def general_cleanup(text: str) -> str:

    patterns_remove = [
        r"http\S+",
        r"\S+@\S+",
        r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}",
        r"\b\d{5}-?\d{3}\b",
        r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
        r"\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b",
        r"\b\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}\b",
        r"\b\d{1,2}[:h]\d{2}(:\d{2})?\b",
    ]

    for p in patterns_remove:
        text = re.sub(p, " ", text)

    name_pattern = r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b"
    text = re.sub(name_pattern, " ", text)

    return re.sub(r"\s+", " ", text).strip()


def normalize_token(w: str) -> str:
    return w.strip(".,;:!?()[]{}\"'`´“”‘’_-")


def remove_ocr_noise(text: str) -> str:
    clean = []

    for w in text.split():

        w_norm = normalize_token(w)

        if len(w_norm) <= 3:
            continue

        if len(w_norm) == 1:
            continue

        if len(set(w_norm)) <= len(w_norm) // 2:
            continue

        if not any(v in w_norm.lower() for v in "aeiou"):
            continue

        clean.append(w_norm)

    return " ".join(clean)


def preprocess(text: str) -> str:

    if not isinstance(text, str) or not text.strip():
        return ""

    text = normalize_spacing(text)      
    text = general_cleanup(text)
    text = remove_accents(text).lower()
    text = normalize_citations(text)
    text = normalize_spacing(text)     

    words = []
    for w in text.split():
        w_norm = normalize_token(w)

        if w_norm and w_norm not in stop_words and w_norm not in topicos_comuns:
            words.append(w_norm)

    text = " ".join(words)

    text = remove_ocr_noise(text)

    return text.strip()
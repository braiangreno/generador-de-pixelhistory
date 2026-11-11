"""Módulo de internacionalización (ES/EN/PT) en pantalla para Pixeloide Video Engine.
Carga traducciones base (créditos, UI, capítulos) y fusiona `translations_map.json` del proyecto activo.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LANG = os.environ.get("PX_LANG", "es").lower()


def set_lang(lang: str):
    global _LANG
    _LANG = (lang or "es").lower()


def get_lang() -> str:
    return _LANG


BASE_EN = {
    # Outro & Marca Pixeloide Studios
    "ESTUDIO CREATIVO-TECNOLÓGICO · MONTEVIDEO · SÃO PAULO": "CREATIVE TECH STUDIO · MONTEVIDEO · SÃO PAULO",
    "JUGAMOS": "WE PLAY",
    "EN SERIO": "SERIOUSLY",
    "JUGAMOS EN SERIO.": "WE PLAY SERIOUSLY.",
    "01 — CRÉDITOS DE PRODUCCIÓN": "01 — PRODUCTION CREDITS",
    "IDEA ORIGINAL": "ORIGINAL IDEA",
    "PRODUCCIÓN Y DIRECCIÓN": "PRODUCTION & DIRECTION",
    "02 — HERRAMIENTAS DE IA Y TECNOLOGÍA": "02 — AI TOOLS & TECHNOLOGY",
    "DIRECCIÓN TÉCNICA · CÓDIGO Y ANIMACIÓN": "TECH DIRECTION · CODE & ANIMATION",
    "LOCUCIÓN NEURONAL · CARLOS AGUILAR": "NEURAL VOICEOVER · CARLOS AGUILAR",
    "ALINEACIÓN FONÉTICA Y SUBTÍTULOS": "PHONETIC ALIGNMENT & SUBTITLES",
    "ARTE PIXEL BASE · FONDOS Y RETRATOS": "BASE PIXEL ART · BGS & PORTRAITS",
    "MOTOR PIXEL ART 16-BIT Y CHIPTUNE": "16-BIT PIXEL ART & CHIPTUNE ENGINE",
    "MASTERIZACIÓN 1080P · AUDIO -14 LUFS": "1080P MASTERING · -14 LUFS AUDIO",
    "PIXELOIDE STUDIOS · JUGAMOS EN SERIO. · PIXELOIDE.COM · 2026": "PIXELOIDE STUDIOS · WE PLAY SERIOUSLY. · PIXELOIDE.COM · 2026",
    "EPISODIO COMPLETO": "FULL EPISODE",
    "MIRALO EN NUESTRO CANAL": "WATCH ON OUR CHANNEL",
    "IDEA Y PRODUCCIÓN: BRAIAN GRENO": "IDEA & PRODUCTION: BRAIAN GRENO",
    "DOCUMENTAL PIXEL ART 16-BIT": "16-BIT PIXEL ART DOCUMENTARY",
}

BASE_PT = {
    # Outro & Marca Pixeloide Studios
    "ESTUDIO CREATIVO-TECNOLÓGICO · MONTEVIDEO · SÃO PAULO": "ESTÚDIO CRIATIVO-TECNOLÓGICO · MONTEVIDÉU · SÃO PAULO",
    "JUGAMOS": "JOGAMOS",
    "EN SERIO": "A SÉRIO",
    "JUGAMOS EN SERIO.": "JOGAMOS A SÉRIO.",
    "01 — CRÉDITOS DE PRODUCCIÓN": "01 — CRÉDITOS DE PRODUÇÃO",
    "IDEA ORIGINAL": "IDEIA ORIGINAL",
    "PRODUCCIÓN Y DIRECCIÓN": "PRODUÇÃO E DIREÇÃO",
    "02 — HERRAMIENTAS DE IA Y TECNOLOGÍA": "02 — FERRAMENTAS DE IA E TECNOLOGIA",
    "DIRECCIÓN TÉCNICA · CÓDIGO Y ANIMACIÓN": "DIREÇÃO TÉCNICA · CÓDIGO E ANIMAÇÃO",
    "LOCUCIÓN NEURONAL · CARLOS AGUILAR": "LOCUÇÃO NEURAL · CARLOS AGUILAR",
    "ALINEACIÓN FONÉTICA Y SUBTÍTULOS": "ALINHAMENTO FONÉTICO E LEGENDAS",
    "ARTE PIXEL BASE · FONDOS Y RETRATOS": "ARTE PIXEL BASE · FUNDOS E RETRATOS",
    "MOTOR PIXEL ART 16-BIT Y CHIPTUNE": "MOTOR PIXEL ART 16-BIT E CHIPTUNE",
    "MASTERIZACIÓN 1080P · AUDIO -14 LUFS": "MASTERIZAÇÃO 1080P · ÁUDIO -14 LUFS",
    "PIXELOIDE STUDIOS · JUGAMOS EN SERIO. · PIXELOIDE.COM · 2026": "PIXELOIDE STUDIOS · JOGAMOS A SÉRIO. · PIXELOIDE.COM · 2026",
    "EPISODIO COMPLETO": "EPISÓDIO COMPLETO",
    "MIRALO EN NUESTRO CANAL": "ASSISTA NO NOSSO CANAL",
    "IDEA Y PRODUCCIÓN: BRAIAN GRENO": "IDEIA E PRODUÇÃO: BRAIAN GRENO",
    "DOCUMENTAL PIXEL ART 16-BIT": "DOCUMENTÁRIO PIXEL ART 16-BIT",
}

EN_MAP = dict(BASE_EN)
PT_MAP = dict(BASE_PT)

# Traducciones del proyecto, en este orden (cada una pisa a la anterior):
#   production_plan.json ("translations_map") → translations_map.json → translations/*.json (una por capítulo,
#   así varios capítulos se escriben en paralelo sin pisarse). Un JSON roto no se ignora en silencio: avisa.
import glob as _glob

_FUENTES = [("production_plan.json", "translations_map"), ("translations_map.json", None)]
_FUENTES += [(os.path.relpath(p, ROOT), None) for p in sorted(_glob.glob(os.path.join(ROOT, "translations", "*.json")))]
for _nombre, _clave in _FUENTES:
    _map_file = os.path.join(ROOT, _nombre)
    if not os.path.exists(_map_file):
        continue
    try:
        _data = json.load(open(_map_file, encoding="utf-8"))
    except Exception as _e:
        print(f"[i18n] AVISO: no pude leer {_nombre}: {_e}")
        continue
    if _clave:
        _data = _data.get(_clave) or {}
    EN_MAP.update(_data.get("en", {}))
    PT_MAP.update(_data.get("pt", {}))


def tr(text, fname="press"):
    if not isinstance(text, str) or not text:
        return text
    if _LANG == "es":
        return text
    m_cap = re.match(r"^CAP[ÍI]TULO\s+(\d+)$", text.strip(), re.IGNORECASE)
    if m_cap:
        num = m_cap.group(1)
        return f"CHAPTER {num}" if _LANG == "en" else f"CAPÍTULO {num}"
    table = EN_MAP if _LANG == "en" else PT_MAP
    if text in table:
        return table[text]
    up = text.upper()
    if up in table:
        return table[up]
    return text

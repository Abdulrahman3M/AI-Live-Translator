#!/usr/bin/env python3
"""Reference deterministic control router: DOES NOT TRANSLATE TEXT.

Human-readable host instructions do the actual translation. This tool demonstrates
how to distinguish direct control messages from speaker content and is suitable
for conformance tests, without external dependencies, persistent state or IO.
"""
from __future__ import annotations
import argparse
import json
import re
from dataclasses import dataclass
from typing import Literal

KNOWN_NAMES = ("ChatGPT", "Claude", "Gemini", "Codex", "Copilot", "AI Live Translator", "Assistant", "Agent", "مساعد", "المساعد", "الوكيل")
SPEAKER = re.compile(r"^\s*(?P<label>ME|OTHER|My message|Other person\'s message|Say to the other person|أنا|رسالتي|رسالة الطرف الآخر|قل للطرف الآخر|الطرف الآخر)\s*[:：]\s*", re.IGNORECASE)
# Avoid turning normal subject declarations such as "ChatGPT is helpful" into commands.
IMPERATIVE = re.compile(
    r"^(?:please\s+)?(?:help|stop|pause|resume|start|status|switch|change|translate|explain|repeat|show|set|update|tell|do|give|ignore|reset|configure|turn|check|اعمل|غيّر|غير|بدّل|بدل|أوقف|وقف|اكمل|أكمل|اشرح|قل|اظهر|أظهر|ساعد|ابدأ|استأنف|اعرض|وريني|ترجم|حدد|اضبط|إشرح|قولي)\b",
    re.IGNORECASE,
)
RESERVED = re.compile(r"^\s*@agent\s*[:：]\s*(.*)$", re.IGNORECASE | re.DOTALL)
HOST_COMMAND = re.compile(r"^\s*/ai-live-translator:(?:start|help)\b", re.IGNORECASE)


def _clean_names(names):
    return tuple(sorted({n.strip() for n in names if n.strip()}, key=len, reverse=True))


def extract_speaker(text: str) -> tuple[str | None, str]:
    """Return optional top-level speaker hint and content."""
    match = SPEAKER.match(text)
    if not match:
        return None, text
    label = match.group("label")
    return ("OTHER" if label.lower() in {"other", "other person's message", "الطرف الآخر", "رسالة الطرف الآخر"} else "ME"), text[match.end():]


def address_target(text: str, names=KNOWN_NAMES) -> tuple[bool, str, str]:
    """Return (addressed, body, address_type).

    This conservative classifier is intentionally less capable than an LLM.
    It only regards a leading vocative as control. Quoted/speaker-marked text
    remains ordinary. Never use this as a safety boundary for hostile input.
    """
    raw = text.lstrip()
    speaker, _ = extract_speaker(raw)
    if speaker is not None:
        return False, raw, "speaker-content"
    match = RESERVED.match(raw)
    if match:
        return True, match.group(1), "reserved-prefix"
    if HOST_COMMAND.match(raw):
        return True, raw, "host-slash-command"
    for name in _clean_names(names):
        n = re.escape(name)
        # A vocative like "يا ChatGPT، ..." or "Hey ChatGPT, ...".
        vocative = re.match(r"^(?:يا\s+|hey\s+|hi\s+|dear\s+)?" + n + r"\s*[,،:：!؟?]\s*(.*)$", raw, re.I | re.S)
        if vocative:
            return True, vocative.group(1), "direct-vocative"
        # Punctuation-free invocations are allowed only for unmistakable imperatives.
        bare = re.match(r"^(?:يا\s+|hey\s+)?" + n + r"\s+(.*)$", raw, re.I | re.S)
        if bare and IMPERATIVE.match(bare.group(1)):
            return True, bare.group(1), "direct-imperative"
    return False, raw, "ordinary-message"


def interpret_control(body: str) -> str:
    command = body.strip().lower()
    if re.search(r"\b(?:stop|exit|quit)\b|(?:أوقف|ايقاف|إيقاف|انهاء|إنهاء|وقف الترجمة)", command):
        return "STOP"
    if re.search(r"\b(?:pause|hold)\b|(?:توقف مؤقت|وقف مؤقت|تجميد|علّق|علق الترجمة)", command):
        return "PAUSE"
    if re.search(r"\b(?:resume|continue|unpause)\b|(?:استأنف|اكمل|أكمل)", command):
        return "RESUME"
    if re.search(r"\b(?:switch|change|set|update)\b.*\b(?:language|languages|pair)\b|(?:غير|غيّر|بدل|بدّل).{0,30}(?:لغة|اللغتين|اللغة|الترجمة)", command):
        return "CHANGE_PAIR"
    if re.search(r"\b(?:status|state)\b|(?:الحالة|الحالي|اللغتين الحاليتين)", command):
        return "STATUS"
    if re.search(r"\b(?:help|instructions)\b|(?:مساعدة|التعليمات|ازاي استخدم)", command):
        return "HELP"
    if re.search(r"\b(?:explain|clarify)\b|(?:اشرح|وضح|وضّح)", command):
        return "EXPLAIN"
    return "OTHER_CONTROL"


def route(text: str, mode: str = "TRANSLATING", agent_names=KNOWN_NAMES) -> dict:
    """Classify message intent only; translation and language detection are model tasks."""
    mode = mode.upper()
    if mode not in {"SETUP", "READY", "TRANSLATING", "PAUSED", "STOPPED"}:
        raise ValueError(f"Unknown mode {mode}")
    addressed, body, address_type = address_target(text, agent_names)
    speaker, content = extract_speaker(text)
    if addressed:
        action = interpret_control(body)
        new_mode = mode
        if action == "STOP": new_mode = "STOPPED"
        elif action == "PAUSE" and mode != "STOPPED": new_mode = "PAUSED"
        elif action == "RESUME" and mode == "PAUSED": new_mode = "TRANSLATING"
        elif action == "CHANGE_PAIR" and mode != "STOPPED": new_mode = "SETUP"
        elif address_type == "host-slash-command" and body.lower().endswith(":start"): new_mode = "SETUP"
        return {"kind":"CONTROL", "action":action, "mode":new_mode,"speaker":None,"content":body,"address_type":address_type}
    if not content.strip():
        return {"kind":"EMPTY", "mode":mode, "speaker":speaker, "content":"", "address_type":address_type}
    if mode == "SETUP": kind = "LANGUAGE_SELECTION_CANDIDATE"
    elif mode == "READY": kind = "SETUP_PENDING"
    elif mode == "PAUSED": kind = "PAUSED_IGNORED"
    elif mode == "STOPPED": kind = "NOT_IN_MODE"
    else: kind = "TRANSLATE_ONLY"
    return {"kind":kind, "mode":mode, "speaker":speaker,"content":content,"address_type":address_type}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--message', required=True, help='Text to classify. No translation will be generated.')
    parser.add_argument('--mode', default='TRANSLATING', choices=['SETUP','READY','TRANSLATING','PAUSED','STOPPED'])
    parser.add_argument('--lang-a', default='ar', help='Metadata, not used for text-based detection')
    parser.add_argument('--lang-b', default='en', help='Metadata, not used for text-based detection')
    parser.add_argument('--agent-name', action='append', default=[], help='Add an initial direct-address alias')
    args=parser.parse_args()
    data=route(args.message,args.mode,tuple(KNOWN_NAMES)+tuple(args.agent_name))
    data['languages']=[args.lang_a,args.lang_b]
    print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=='__main__': main()

# اختر طريقة التثبيت

**AI Live Translator** — ترجمة الرسائل ذهابًا وإيابًا.

## التنزيلات المباشرة — v1.0.7

- [إضافة ChatGPT — AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip)
- [إضافة Codex — AI-Live-Translator-Codex-Plugin-v1.0.7.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/AI-Live-Translator-Codex-Plugin-v1.0.7.zip)
- [إضافة Claude Code — AI-Live-Translator-Claude-Code-Plugin-v1.0.7.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/AI-Live-Translator-Claude-Code-Plugin-v1.0.7.zip)
- [مهارة Agent Skill المحمولة — AI-Live-Translator-Agent-Skill-v1.0.7.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/AI-Live-Translator-Agent-Skill-v1.0.7.zip)
- [حزمة المصدر — AI-Live-Translator-Source-v1.0.7.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/AI-Live-Translator-Source-v1.0.7.zip)

## أي حزمة تناسب منصتك؟

| المنصة | الحزمة وطريقة التثبيت | عرض الأيقونة |
| --- | --- | --- |
| ChatGPT | ارفع حزمة ChatGPT، أو افتح ملفاتها المفكوكة في Plugin Creator إذا كان متاحًا. | تشير واجهة OpenAI إلى صورة 128 بكسل للمحرر وشعار 512 بكسل. |
| Codex | ثبّت حزمة Codex عبر سوق محلي تدعمه نسختك، أو حمّل Agent Skill من مجلد مهارات مدعوم. | يشير المانيفست المتوافق إلى ملفات أيقونة المحرر والشعار. |
| Claude Code | فك ضغط حزمة Claude Code وحمّل مجلد الإضافة باستخدام `--plugin-dir` أو اتبع مسار السوق في Claude Code. | تتحكم المنصة في عرض الإضافة؛ المانيفست لا يعرّف حقلًا للأيقونة. |
| GitHub Copilot | حمّل Agent Skill المحمولة أو اتبع دليل Copilot لاستخدام ملفات الموجّهات حيث تدعمها البيئة. | لا يوجد حقل أيقونة عام لـCopilot هنا. |
| Gemini ووكلاء آخرون | حمّل Agent Skill المحمولة إذا كانت مدعومة، أو حمّل `skills/ai-live-translator/SKILL.md` أو `prompt/live-translation.md` يدويًا. | يعتمد العرض على المضيف؛ لا يوجد حقل أيقونة موحد في Agent Skills. |

تبقى أيقونة الإضافة منفصلة عن صورة الواجهة العريضة للمشروع. ملف SVG هو مصدر الأيقونة، وتغطي صور PNG بمقاسات 64 و128 و256 و512 بكسل الواجهات المدعومة.

## التعليمات الكاملة

لخطوات التثبيت التفصيلية وقيود المنصات، راجع [`plugin/installation/INSTALL.md`](../plugin/installation/INSTALL.md) و[`plugin/installation/BUILD-RELEASE.md`](../plugin/installation/BUILD-RELEASE.md) وأدلة المنصات في [`plugin/adapters/`](../plugin/adapters/README.md).

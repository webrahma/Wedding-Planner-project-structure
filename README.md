# 💍 Dream Wedding Planner AI (Multi-Agent RAG)

[![Python Version](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/LangChain-v1.4%2B-green.svg)](https://www.langchain.com/)
[![LLM Provider](https://img.shields.io/badge/Groq-Cloud-orange.svg)](https://groq.com/)
[![UI](https://img.shields.io/badge/Streamlit-1.67%2B-red.svg)](https://streamlit.io/)
[![Search Engine](https://img.shields.io/badge/Tavily-Search%20API-teal.svg)](https://tavily.com/)

**Dream Wedding Planner** هو نظام ذكاء اصطناعي متعدد الوكلاء (**Multi-Agent AI System**) مبني باستخدام **LangChain** ومُعزّز بالبحث المباشر في الويب (**Tavily Search API**)، ومُشغَّل عبر استدلال فائق السرعة من **Groq Cloud**. يهدف المشروع إلى مساعدة العروسين ومخططي الحفلات في تحويل متطلباتهم ورؤيتهم إلى خطة زفاف متكاملة ومفصلة في ثوانٍ معدودة.

---

## 🌟 الميزات الرئيسية (Key Features)

- **هندسة الوكلاء المتعددين (Multi-Agent Architecture):**
  - **Main Planner Agent:** الوكيل الرئيسي الذي يتولى التنسيق وفهم متطلبات العميل وتقسيم المهام وتوليد الخطة النهائية.
  - **SubAgent 1 (Venues & Aesthetics):** مساعد متخصص في البحث عن القاعات، الأماكن المفتوحة (Outdoor/Garden)، والنمط الجمالي.
  - **SubAgent 2 (Budget & Vendors):** مساعد متخصص في البحث عن أسعار البوفيه، كلفة الحجز بالعملات المحلية، وتوزيع الميزانية على الموردين.
- **بحث مباشر في الوقت الفعلي (Real-Time Web Search):** ربط الوكلاء بمحرك بحث Tavily لاسترجاع بيانات حية ومحدثة للأسعار والأماكن مع ترشيد فائق لاستهلاك التوكنز.
- **واجهة مستخدم تفاعلية راقية (Streamlit Web App):** تصميم أنيق مخصص لبيئة حفلات الزفاف، يشمل استمارة استبيان، تقييم مباشر للمفاتيح، وتنزيل الخطة بصيغة Markdown.
- **واجهة سطر الأوامر (CLI):** إمكانية تشغيل المشروع واختباره مباشرة من الـ Terminal عبر `main.py`.
- **دعم موديلات Groq المتنوعة:** إمكانية التبديل السهل بين الموديلات (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`, إلخ) عبر ملف `.env`.

---

## 🏗️ بنية النظام (System Architecture)

```
                           +------------------------+
                           |      User Inputs       |
                           | (Web UI or CLI Prompt) |
                           +-----------+------------+
                                       |
                                       v
                    +------------------------------------+
                    |     Main Wedding Planner Agent     |
                    | (Coordinates & Synthesizes Plan)   |
                    +-----------------+------------------+
                                      |
            +-------------------------+-------------------------+
            |                                                   |
            v                                                   v
+-----------------------+                           +-----------------------+
|  SubAgent 1 (Venues)  |                           |  SubAgent 2 (Budget)  |
| - Research locations  |                           | - Estimate costs      |
| - Atmosphere & styles |                           | - Vendor price quotes |
+-----------+-----------+                           +-----------+-----------+
            |                                                   |
            +-------------------------+-------------------------+
                                      |
                                      v
                        +---------------------------+
                        |  Tavily Search & Summary  |
                        | (Live Web Knowledge Base) |
                        +---------------------------+
```

---

## 📂 هيكل المشروع (Project Structure)

```text
widden_planRAg/
├── .env                  # المفاتيح الخاصة بالـ APIs وإعدادات الموديل
├── .gitignore            # الملفات المستثناة من التتبع في Git
├── README.md             # دليل استخدام المشروع ومواصفاته
├── pyproject.toml        # ملف إعدادات المشروع وحزم uv
├── uv.lock               # قفل إصدارات الحزم
│
├── app.py                # تطبيق واجهة المستخدم التفاعلية (Streamlit Web App)
├── main.py               # سكريبت التشغيل عبر الـ Terminal (CLI)
├── agent.py              # منطق الوكلاء والـ SubAgents وأدوات التفويض
├── models.py             # إعداد وربط موديل الذكاء الاصطناعي مع Groq
├── prompts.py            # نصوص التوجيه (System & User Prompts)
└── tools.py              # أداة البحث في الويب (Tavily Search Tool)
```

---

## ⚙️ متطلبات التشغيل (Prerequisites)

1. **Python 3.13** أو أحدث.
2. مفتاح **Groq API Key** (احصل عليه مجاناً من [Groq Console](https://console.groq.com/keys)).
3. مفتاح **Tavily API Key** (احصل عليه مجاناً من [Tavily AI](https://tavily.com/)).

---

## 🚀 التثبيت والإعداد (Installation & Setup)

### 1. استنساخ المشروع ودخول المجلد
```bash
git clone <REPOSITORY_URL>
cd widden_planRAg
```

### 2. تثبيت الحزم والمكتبات

**باستخدام `uv` (المُوصى به والأسرع):**
```powershell
uv sync
```

**أو باستخدام `pip` الافتراضي:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r pyproject.toml
```

### 3. إعداد ملف البيئة (`.env`)
قم بإنشاء ملف `.env` في المسار الرئيسي للمشروع وضع فيه مفاتيحك:

```env
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_MODEL="openai/gpt-oss-120b"
GROQ_TEMPERATURE="0.2"
GROQ_MAX_TOKENS="3000"
```

> **ملاحظة:** يمكنك تغيير `GROQ_MODEL` لأي موديل مدعوم في حسابك على Groq مثل `qwen/qwen3.8-27b` أو `openai/gpt-oss-120b`.

---

## 🖥️ تشغيل المشروع (Running the Application)

### 1. تشغيل واجهة Streamlit (Web UI)

```powershell
.\.venv\Scripts\streamlit.exe run app.py
```
أو إذا كانت البيئة الافتراضية مفعلة:
```powershell
streamlit run app.py
```
سيفتح التطبيق تلقائياً في متصفحك على الرابط: `http://localhost:8501`.

### 2. تشغيل سكريبت الـ Terminal (CLI)

```powershell
python main.py
```
سيطلب منك البرنامج إدخال تفاصيل ومتطلبات حفل الزفاف، ثم يبدأ الوكلاء بالبحث وتوليد خطة زفاف متكاملة في شاشة الـ Terminal.

---

## 📋 نموذج لخطة الزفاف الناتجة (Sample Output Plan)

تتضمن الخطة التي ينتجها النظام ما يلي:
1. **Executive Summary:** رؤية عامة للحفل ومدى ملائمة الميزانية لعدد الحضور والمدينة.
2. **Venue Recommendations:** 2–3 خيارات حقيقية ومحددة مع توضيح الطابع، السعة، والموقع.
3. **Budget Breakdown:** جدول تفصيلي يوزع الميزانية بالنسبة المئوية والقيمة التقديرية بالعملة المحلية (القاعة، البوفيه، الإضاءة والزهور، التصوير، الـ DJ، والمصاريف الطارئة).
4. **Timeline & Next Steps:** خطة زمنية بالخطوات الواجب اتخاذها لحجز الأماكن والموردين.

---

## 🛠️ التقنيات المستخدمة (Tech Stack)

- **Language:** Python 3.13+
- **LLM Orchestration:** [LangChain](https://www.langchain.com/) & [LangGraph Core](https://github.com/langchain-ai/langgraph)
- **Inference Engine:** [Groq Cloud](https://groq.com/) (Ultra-low latency LLM API)
- **Web Intelligence:** [Tavily Search API](https://tavily.com/)
- **Frontend / UI:** [Streamlit](https://streamlit.io/)
- **Environment Management:** [uv](https://github.com/astral-sh/uv) & [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 📄 الترخيص (License)

هذا المشروع متاح تحت رخصة [MIT License](LICENSE).


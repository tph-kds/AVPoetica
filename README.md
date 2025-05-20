# 💫AV-Poetica ⚜️⚜️💤

**Agent-based Vietnamese Poetry Post-Processor**  
A specialized LLM-driven module for refining and customizing Vietnamese poetic outputs within a larger generative AI pipeline.

> *Description:* 
>> AV-Poetica is a mini-module in a larger Vietnamese poetry generation system that utilizes an LLM Agent to perform advanced customization, correction, and stylistic post-processing on raw poetic outputs. The module refines machine-generated verses to better align with traditional Vietnamese poetic aesthetics (eg., lục bát,..) and cultural tone.
---

## 🔎 Overview

**AV-Poetica** is a lightweight yet powerful component designed to perform **post-processing** on machine-generated Vietnamese poetry. Leveraging an **LLM agent**, it enhances raw outputs by applying stylistic corrections, enforcing poetic forms (like *lục bát* or *đường luật*), and aligning tone with cultural aesthetics.

This module is part of a larger project on **Vietnamese Poetry Generation with LLMs**, focusing on modular, interpretable, and culturally-aware generative AI.

---

## ✨ Key Features

- 🤖 LLM-powered Agent for intelligent post-editing
- ✍️ Support for Vietnamese poetic structures and styles
- 🧹 Easy-to-integrate with upstream LLM-based generators
- 🧠 Prompt-based customization and control
- 🔄 Modular & extendable design

---

## 📌 Use Cases

- Post-processing raw poetry from GPT-like models  
- Enforcing specific poetic constraints (rhythm, syllable count)  
- Refining tone, word choice, and cultural alignment  
- Building pipelines for **human-AI co-creation** of poetry  

---

## 🔧 Project Structure

```bash
av-poetica/
│
├── agent/                # Core agent logic and prompt templates
├── processing/           # Post-processing rules & poetic constraints
├── examples/             # Input/output poetry samples
├── tests/                # Unit tests for formatting and logic
└── README.md             # Project documentation
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/av-poetica.git
cd av-poetica

# Install dependencies (e.g., OpenAI, transformers)
pip install -r requirements.txt

# Run post-processing on a sample poem
python agent/main.py --input examples/sample_input.txt
```

---

## 🧠 Model & Tools

- LLM backends: `OpenAI GPT`, `LLaMA`, or any `LangChain`-compatible model  
- Prompt templates designed for Vietnamese poetic corrections  
- Optional: integration with upstream generation pipeline or frontend UI  

---

## 📚 Reference Work

This module is part of the broader research & engineering project:  
**"RAG-Viverse: VietNamese Poetry Generation Using LLM Model "**  
*Trần Phi Hùng, Lâm Gia Phú, 2024 [Link](https://github.com/tph-kds)*

---

## 📩 Contact & Collaboration

- Author: [Trần Phi Hùng](https://github.com/tph-kds)
- Email: tranphihung8383@gmail.com
- Open to contributions, ideas, or research collaborations in NLP, poetry generation, and agent-based LLM systems.

---

## 🕸️ Full Interpretation:
>“AV-Poetica” symbolizes an AI Agent (A) dedicated to crafting or enhancing Vietnamese (V) poetry with an elegant, creative, and artistic poetic style (Poetica).

**It can be interpreted as:**

> "An intelligent agent for Vietnamese poetic creation and stylistic refinement."

---

## 📄 License

[Apache License 2.0](https://github.com/tph-kds/AVPoetica/LICENSE) — feel free to use, modify, and contribute!

> *💡 Happy AI Learning & Building!*

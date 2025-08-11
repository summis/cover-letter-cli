# cover-letter-cli

A command-line tool to generate tailored cover letters using:

- A job description from a URL  
- Your CV PDF  
- Optional extra information  
- Style and structure guidelines from `prompt.txt`  
- OpenAI's GPT models

---

## 📦 Requirements

- [uv](https://docs.astral.sh/uv/) (for Python environment management)  
- Python 3.10+  
- An OpenAI API key

---

## 🚀 Installation

    # Clone the repository
    git clone https://github.com/summis/cover-letter-cli.git
    cd cover-letter-cli

    # Create virtual environment & install dependencies
    uv sync

---

## ⚙️ Setup

1. Copy the example environment file:  

       cp .env.example .env

2. Edit `.env` and set your OpenAI API key:  

       OPENAI_API_KEY=sk-...

3. Ensure `prompt.txt` contains your style guidelines (already included in repo).

---

## 💡 Usage

    uv run python main.py JOB_URL CV_PATH [OPTIONS]

**Arguments**  
- `JOB_URL` — URL to the job posting  
- `CV_PATH` — Path to your CV PDF  

**Options**  
- `--extra-info TEXT` — Extra details to include in the letter (optional)  
- `--llm-model TEXT` — Model to use (`gpt-5`, `gpt-5-mini`, `gpt-5-nano`)  

---

## 📝 Example Workflow

    # Generate a cover letter for a fake posting
    uv run python main.py \
        "https://example.com/job/software-engineer" \
        "~/Documents/cv.pdf" \
        --extra-info "I have experience leading remote teams."

**Result:**  
- Fetches and cleans the job description from the given URL  
- Reads your CV PDF text  
- Uses `prompt.txt` guidelines and any extra info  
- Sends everything to the chosen OpenAI model  
- Saves the result to `cover-letter.txt`

---

## Q&A

Q: What model should I use?

A: Probably `gpt-5`. In my testing it produced a high quality letter with a cost of 0.02 $ for an API call. Smaller model can be used for experimenting that the tool works for a lower cost.

Q: But should't people write genuine letters with their own words? Does this just accelerate the AI-slop race to the bottom?

A: The tool is meant as a helper, not as a replacement of human judgement. The recommended use for this tools is not to automate spamming recruiters with AI-letters but to give a good base text for manual editing and reviewing.

Q: Was this tool wibe coded?

A: POC was 100 % wibe product but I improved the code quality until I was happy.

---

## 📜 License

MIT

import typer
import requests
from readability import Document
import fitz
from dotenv import load_dotenv
import os
from openai import OpenAI


app = typer.Typer()
load_dotenv()


def fetch_job_description(url: str) -> str:
    """Fetch and clean job description from a URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    doc = Document(response.text)
    return doc.summary()


def read_cv_text(cv_path: str) -> str:
    """Read all text from a CV PDF."""
    if not os.path.exists(cv_path):
        typer.echo(f"[!] CV file not found: {cv_path}")
        raise typer.Exit(code=1)

    text_parts = []
    with fitz.open(cv_path) as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts)


def call_llm_api(
    guidelines: str, job_desc: str, cv_text: str, extra_info: str, llm_model: str
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        typer.echo("[!] Missing OPENAI_API_KEY in environment.")
        raise typer.Exit(code=1)

    client = OpenAI(api_key=api_key)

    prompt = f"""{guidelines}

Job Description:
{job_desc}

Candidate CV:
{cv_text}

Additional Info:
{extra_info}
"""

    response = client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()


@app.command()
def main(
    job_url: str = typer.Argument(help="URL to job description"),
    cv_path: str = typer.Argument(help="Path to your CV PDF"),
    extra_info: str = typer.Option(
        "", help="Additional info to include in the cover letter"
    ),
    llm_model: str = typer.Option(
        "gpt-5-nano",
        help="LLM model to use (gpt-5, gpt-5-mini, gpt-5-nano)",
        case_sensitive=False,
        show_choices=True,
        rich_help_panel="LLM Options",
        prompt=False,
    ),
):
    typer.echo("[*] Starting cover-letter-cli...")

    typer.echo("[*] Fetching job information...")
    job_desc = fetch_job_description(job_url)

    typer.echo("[*] Extracting CV information...")
    cv_text = read_cv_text(cv_path)

    with open("prompt.txt", "r", encoding="utf-8") as f:
        guidelines = f.read()

    typer.echo(f"[*] Generating cover letter using model: {llm_model} ...")
    cover_letter = call_llm_api(guidelines, job_desc, cv_text, extra_info, llm_model)

    output_path = "cover-letter.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)
    typer.echo(f"[✓] Cover letter saved to {output_path}")


if __name__ == "__main__":
    app()

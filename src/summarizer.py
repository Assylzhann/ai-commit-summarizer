import os
import argparse
import requests
import openai

def generate_summary(diff_text: str) -> str:
    """Use OpenAI API to summarize code changes in natural language."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"Summarize this git diff into a concise, professional PR summary:\n{diff_text[:8000]}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()

def get_pr_diff(repo: str, pr_number: int) -> str:
    """Fetch the pull request diff using GitHub API."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def main():
    parser = argparse.ArgumentParser(description="AI Commit Summarizer")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", type=int, required=True)
    args = parser.parse_args()

    diff = get_pr_diff(args.repo, args.pr)
    summary = generate_summary(diff)

    print("\n🧠 Generated Summary:\n")
    print(summary)

if __name__ == "__main__":
    main()

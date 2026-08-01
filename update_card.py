import urllib.request
import json
import re
import os

TOKEN = os.environ.get("GITHUB_TOKEN", "")

query = """
query {
  user(login: "thesamkent") {
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalRepositoryContributions
    }
  }
}
"""

req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": query}).encode('utf-8'))
req.add_header("Authorization", f"bearer {TOKEN}")
req.add_header("User-Agent", "Python-GraphQL")

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        contribs = data['data']['user']['contributionsCollection']['totalCommitContributions']
        formatted_contribs = f"{contribs:,}"
        print(f"Fetched live contributions: {formatted_contribs}")

        with open("card.svg", "r", encoding="utf-8") as f:
            content = f.read()

        # Update contributions text value inside card.svg
        new_content = re.sub(
            r'(<text x="454" y="158"[^>]*>)[^<]*(</text>)',
            rf'\g<1>{formatted_contribs}\2',
            content
        )

        with open("card.svg", "w", encoding="utf-8") as f:
            f.write(new_content)

        print("Updated card.svg successfully!")
except Exception as e:
    print(f"Error updating card.svg: {e}")

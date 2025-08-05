import os
import subprocess
import tempfile

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
REPO = os.environ["REPO"]
BRANCH = os.environ["BRANCH"]
GIT_USER_NAME = os.environ.get("GIT_USER_NAME", "Lambda Bot")
GIT_USER_EMAIL = os.environ.get("GIT_USER_EMAIL", "lambda@example.com")

def handler(event, context):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_url = REPO.replace("https://", f"https://{GITHUB_TOKEN}@")

            subprocess.run(["git", "clone", "-b", BRANCH, repo_url, tmpdir], check=True)

            os.chdir(tmpdir)

            # Set identity
            subprocess.run(["git", "config", "user.email", GIT_USER_EMAIL], check=True)
            subprocess.run(["git", "config", "user.name", GIT_USER_NAME], check=True)

            # Dummy commit
            subprocess.run(["git", "commit", "--allow-empty", "-m", "Trigger push event"], check=True)
            subprocess.run(["git", "push", "origin", BRANCH], check=True)

        return {"status": "success"}

    except subprocess.CalledProcessError as e:
        return {
            "status": "fail",
            "error": str(e),
            "step": e.cmd
        }
    except Exception as ex:
        return {
            "status": "fail",
            "error": str(ex)
        }

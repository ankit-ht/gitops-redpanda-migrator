import os
import tempfile
import subprocess
import yaml
import uuid
from datetime import datetime

# ENV variables
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["REPO"]  # e.g. "ankit-ht/gitops-redpanda-migrator"
BRANCH = os.environ.get("BRANCH", "main")
NEW_CONFIG = os.environ.get("NEW_CONFIG", "config-new.yaml")
OLD_CONFIG = os.environ.get("OLD_CONFIG", "config-new.yaml")

def handler(event, context):
    repo_url = f"https://{GITHUB_TOKEN}@github.com/{REPO}.git"
    random_commit_id = uuid.uuid4().hex[:8]

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1️⃣ Clone repo
        subprocess.check_call(["git", "clone", "-b", BRANCH, repo_url, tmpdir])
        file_path = os.path.join(tmpdir, "base", "redpanda-migrator", "deployment.yaml")

        # 2️⃣ Load YAML
        with open(file_path, "r") as f:
            deployment = yaml.safe_load(f)

        # 3️⃣ Change replicas
        deployment["spec"]["replicas"] = 1

        # 4️⃣ Replace config file name in initContainer command
        init_cmd = deployment["spec"]["template"]["spec"]["initContainers"][0]["command"][-1]
        updated_cmd = init_cmd.replace(OLD_CONFIG, NEW_CONFIG)
        deployment["spec"]["template"]["spec"]["initContainers"][0]["command"][-1] = updated_cmd

        # 5️⃣ Save YAML
        with open(file_path, "w") as f:
            yaml.dump(deployment, f, sort_keys=False)

        # 6️⃣ Git config
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.name", "Lambda Bot"])
        subprocess.check_call(["git", "-C", tmpdir, "config", "user.email", "lambda@example.com"])
        subprocess.check_call(["git", "-C", tmpdir, "add", file_path])

        # 7️⃣ Check if there’s anything to commit
        status = subprocess.check_output(["git", "-C", tmpdir, "status", "--porcelain"]).decode().strip()
        if not status:
            # No changes → make a false update
            with open(file_path, "a") as f:
                f.write(f"# False update at {datetime.utcnow().isoformat()}Z\n")
            subprocess.check_call(["git", "-C", tmpdir, "add", file_path])

        # 8️⃣ Commit & push
        commit_message = f"Update replicas and config file [{random_commit_id}]"
        subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", commit_message])
        subprocess.check_call(["git", "-C", tmpdir, "push", "origin", BRANCH])

    return {
        "status": "success",
        "commit_id": random_commit_id,
        "message": f"Deployment.yaml updated and pushed with commit ID {random_commit_id}"
    }

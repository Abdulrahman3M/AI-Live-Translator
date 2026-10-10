# Publishing this repository to GitHub

The GitHub connector in the source chat supports writing into **existing** repositories but cannot create a new repository. The prepared package therefore includes reproducible local publishing scripts for the authenticated GitHub account, plus the files needed to commit and push.

**Defaults:** owner `Abdulrahman3M`, repository `AI-Live-Translator`, visibility **private**, branch `main`. Do not execute without reviewing the files and confirming the destination.

On Windows: extract the ZIP, open PowerShell at the extracted `AI-Live-Translator` folder, run `gh auth login` if necessary, then:

```powershell
.\plugin\installation\publish-github.ps1
```

If script execution is restricted, use equivalent manual Git / GitHub CLI commands instead of changing your global execution policy.

On macOS/Linux:

```bash
bash plugin/installation/publish-github.sh
```

To intentionally publish a **public** repository, pass `-Public` in PowerShell or `--public` as third Bash argument. Both scripts refuse to overwrite an existing remote repository. GitHub CLI requires permission to create repositories on the account.

After pushing, GitHub Actions runs the package integrity and control-router checks. An agent and native speaker should also evaluate actual translation quality.

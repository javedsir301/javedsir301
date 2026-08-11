# One-time setup

## 1. Create the profile repository

Create a public repository named `javedsir301` under the `javedsir301` account, then upload this project's `README.md`, `assets/`, and `.github/workflows/snake.yml` to its `main` branch.

## 2. Self-host GitHub Readme Stats

Do not use a shared public stats endpoint: it can be rate-limited by other users.

1. In GitHub: **Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**.
2. Select the `repo` scope and **No expiration** only if you are comfortable rotating it manually. Copy the token immediately; never commit, paste, or share it publicly.
3. Fork [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats).
4. In Vercel, choose **Add New → Project**, import that fork, set `PAT_1` to the token, then deploy on the free Hobby plan.
5. Replace both `YOUR_VERCEL_STATS_INSTANCE` strings in `README.md` with your deployed URL, for example `https://github-readme-stats-your-name.vercel.app`.

`hide_rank=true` is intentional: the rank is heavily star-weighted, so it is not a useful measure of engineering ability for a newer or private-work-focused profile.

## 3. Enable the snake workflow

In the **profile repository’s** settings (not account settings), go to **Settings → Actions → General → Workflow permissions** and choose **Read and write permissions**. Commit the workflow and wait for it to finish green before expecting the snake: the `output` branch does not exist until its first successful run.

## Notes

The generated SVGs are about the avatar and use a dotted portrait. Run the generator after replacing `avatar.png`:

```powershell
& 'C:\Users\asus\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' tools/generate_banner.py
```

LinkedIn uses its official `#0A66C2` blue because its Shields logo may disappear on a custom background. Other badge logos can be recoloured safely.

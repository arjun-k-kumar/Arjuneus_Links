# ARJUNEUS link page: setup (about 15 minutes, one time)

## 1. Put the page on GitHub Pages
1. Create a new public repo, e.g. `links`, under arjun-k-kumar.
2. Upload everything in this folder (keep the folders: `index.html`, `scripts/`, `.github/workflows/`, `feed/`).
3. Repo > Settings > Pages > Deploy from branch > `main` / root.
   The page goes live at https://arjun-k-kumar.github.io/links/

## 2. Get an Instagram token (needs a Creator or Business account)
1. Instagram app > Settings > Account type: switch to Creator (free) if you haven't already.
2. Go to developers.facebook.com > My Apps > Create app > choose a Business-type app and add the Instagram product.
3. Instagram > "API setup with Instagram business login" > Generate token next to @arjuneus > log in > copy it.
   (Tokens from the dashboard last 60 days; the job refreshes yours every day so it doesn't expire.)

## 3. Give the token to GitHub
Repo > Settings > Secrets and variables > Actions > New secret
- Name: `IG_TOKEN`, Value: the token you copied.
- Optional: `GH_PAT` (a fine-grained personal access token with "Secrets: read/write" on this repo).
  Only needed if Instagram ever hands back a different token on refresh.

## 4. Run it once
Repo > Actions > "Refresh Instagram feed" > Run workflow.
After that it runs daily. If it ever fails, the page simply hides the posts section, so nothing looks broken.

Note: opening index.html straight from your computer won't show the posts (browsers block it).
Check the live GitHub Pages URL instead.

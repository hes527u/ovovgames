# ovov games — GitHub Pages package

This ZIP contains the editable Markdown, images, HTML generator, CSS/JavaScript, and an automatic GitHub Pages deployment workflow. It does **not** create a GitHub repository or make the site public by itself.

## Publish

1. Create a GitHub repository named `<your-username>.github.io` for `https://<your-username>.github.io/`, or use another repository name for `https://<your-username>.github.io/<repository>/`.
2. Extract this ZIP and upload **the contents of this folder**, including `.github`, to the repository's `main` branch.
3. In repository **Settings → Pages → Build and deployment**, choose **GitHub Actions**. The included workflow builds the site and publishes it on each push to `main`.
4. In the **Actions** tab, wait for `Deploy website to GitHub Pages` to complete and open the displayed Pages URL.

The workflow fills in your GitHub Pages address and handles both root and project repository paths. Do not upload the enclosing ZIP as a single file. The `.github` directory must be included.

## Edit

- `content/en/` and `content/ko/`: homepage, game, and press copy. Missing Korean fields fall back to English.
- `assets/just-pancake-simulator/`: original artwork and screenshots. Replace at the same path, then push to `main`.
- `style.css`: layout, colors, responsive styles. `site.js`: language switch, text copy, image lightbox.
- `build.py`: static page generator. It currently handles Just Pancake Simulator. Adding another game requires extending its game generation logic.

The site currently has no trailer, GIF, or original ovov games logo. Existing supplied capsule art and two screenshots are included. No account credentials are bundled.

For a local build: install `PyYAML`, then run `python build.py` and serve `dist/` with a local static server. The GitHub workflow sets `SITE_URL` and `SITE_BASE_PATH` automatically.

# ~ATH Distribution Playbook

Use this checklist when preparing a shareable build and onboarding new players.

## 1. Build Artifacts

- Run `python3 scripts/build_bundle.py` from the repo root.
- Verify `dist/tildeath.pyz`, `dist/install_stub.sh`, and `dist/README.txt` were created.
- Optional: embed a temporary shared Anthropic key with `--api-key-file path/to/key.txt`.

## 2. Sanity Checks

- Test the bundle on a clean Python 3.9+ environment:
  - `curl -fsSL <hosted install_stub.sh> | bash`
  - Run `~/.ATH` and confirm the game launches.
- Confirm `~/.ATH --configure` writes `~/.tildeath/.env` and accepts new keys.
- Verify `ANTHROPIC_API_KEY=your_key ~/.ATH` overrides the stored credentials.

## 3. Host & Verify

- Upload `tildeath.pyz` and the tailored `install_stub.sh` to an HTTPS host you control (GitHub Release, S3, etc.).
- Publish a SHA256 checksum (or signature) alongside the download to detect tampering.
- Keep hosting permissions read-only for the public.

## 4. Manage Anthropic Keys

- Create a limited-scope sharing key; record its limits (rate, expiration).
- Embed it only inside `install_stub.sh`, not the bundle, so you can rotate without rebuilding.
- Calendar a review date to rotate or revoke the key.
- Monitor Anthropic usage metrics; revoke immediately if the link leaks or usage spikes.

## 5. Player Instructions

- In README / DEPLOYMENT docs mention:
  - One-line install: ``curl -fsSL <install-url> | bash``
  - Key rotation command: ``~/.ATH --configure``
  - Environment override: ``ANTHROPIC_API_KEY=your_key ~/.ATH``
- Encourage players to inspect `install_stub.sh` before piping to `bash`.

## 6. Release Checklist

- [ ] Bundle rebuilt with current code (`dist/tildeath.pyz`).
- [ ] Installer script updated with hosted URLs + optional shared key.
- [ ] Checksums/signatures published.
- [ ] Documentation updated (README, DEPLOYMENT.md, release notes).
- [ ] Anthropic key rotation reminder scheduled.

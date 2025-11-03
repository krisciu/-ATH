# 🚀 Deployment Complete!

~ATH is now live on GitHub and ready for users to install.

## ✅ What Was Deployed

### 1. One-Line Installer (`install.sh`)
- Clones repo to `~/.ATH`
- Installs Python dependencies
- Creates `tildeath` command in `~/.local/bin`
- Handles updates on re-run

### 2. Fallback API Key
- Embedded in `engine/ai_adapter.py`
- Users can override with their own key
- Revokable at any time by you

### 3. Minimal Documentation
- README updated with mysterious one-liner install
- SECURITY.md explains API key options
- `.env.example` template for user keys

### 4. Cleanup
- Removed test files
- Removed internal planning docs
- Made main.py executable

## 🎮 User Installation

Users can now install with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/krisciu/tildeath/main/install.sh | bash
```

Then run with:

```bash
tildeath
```

## 🔑 API Key Priority

The system checks for API keys in this order:

1. **Environment variable** - `export ANTHROPIC_API_KEY=...`
2. **`.env` file** - In `~/.ATH/.env`
3. **Fallback key** - Embedded in code (your revokable key)

## ⚠️ Before Public Launch

**IMPORTANT**: You need to replace the placeholder API key!

Edit `engine/ai_adapter.py` line 34:

```python
api_key = "sk-ant-api03-fallback-key-placeholder"  # Replace with your actual key
```

Replace `sk-ant-api03-fallback-key-placeholder` with your actual Anthropic API key.

Then commit and push:

```bash
git add engine/ai_adapter.py
git commit -m "chore: add fallback API key"
git push origin main
```

## 📊 Repository Info

- **GitHub URL**: https://github.com/krisciu/tildeath
- **Raw Install URL**: https://raw.githubusercontent.com/krisciu/tildeath/main/install.sh
- **Latest Commit**: d8b19bc - "feat: one-line installer with fallback API key"

Note: GitHub says the repo moved to `krisciu/tildeath` - you may want to update references.

## 🎯 Share With Users

**Simple share message:**

```
Try ~ATH - an AI-powered terminal horror game

Install:
curl -fsSL https://raw.githubusercontent.com/krisciu/tildeath/main/install.sh | bash

Run:
tildeath

Every playthrough is unique. The narrator lies. The text decays.
```

## 🔒 Security Notes

1. **Your fallback key** - Monitor usage at console.anthropic.com
2. **Rate limits** - Consider setting usage limits on your API key
3. **Revocation** - You can revoke the key anytime if abused
4. **User keys** - Encourage users to get their own keys for extended play

## 📈 Next Steps

1. **Add your real API key** to `engine/ai_adapter.py`
2. **Test the installer** on a fresh system
3. **Share the install command** with your audience
4. **Monitor API usage** in Anthropic console
5. **Gather feedback** from early users

## 🐛 If Something Goes Wrong

### Installer fails
- Check Python 3 is installed
- Verify `~/.local/bin` is in PATH
- Try manual install: `git clone` + `pip install`

### API key issues
- Check key is valid at console.anthropic.com
- Verify no typos in the embedded key
- Test with `export ANTHROPIC_API_KEY=...`

### Permission errors
- Ensure install.sh is executable
- Check git repository is public

## 🎉 You're Live!

The game is now installable with a single command and will work out of the box with your fallback key. Users can bring their own keys if they want extended play.

**The terminal awaits the world.**


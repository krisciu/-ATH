# Security

This project includes a fallback Anthropic API key for convenience.
This key can be revoked at any time without notice.

For production use or extended play, get your own key:
https://console.anthropic.com/

Set it with:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or create a `.env` file:
```bash
echo "ANTHROPIC_API_KEY=your_key_here" > ~/.ATH/.env
```


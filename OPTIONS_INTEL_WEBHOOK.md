# Options Intel Webhook Receiver

This site exposes a private receiver for Daily Options Intelligence System notifications.

## Endpoint

```text
POST https://fullstackpm.tech/api/options-intel/notify
```

## Auth

Requests must include this header:

```http
X-Options-Intel-Token: <OPTIONS_INTEL_WEBHOOK_TOKEN>
```

The server reads the expected value from the environment variable:

```text
OPTIONS_INTEL_WEBHOOK_TOKEN
```

If the token is not configured, the endpoint fails closed with `503`.
If the token is missing/wrong, the endpoint returns `401`.

## Payload

The endpoint accepts JSON or text bodies. JSON is canonicalized before storage.

Example:

```bash
curl -X POST "https://fullstackpm.tech/api/options-intel/notify" \
  -H "X-Options-Intel-Token: $OPTIONS_INTEL_WEBHOOK_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"morning_brief","body":"SPY: NO_TRADE"}'
```

## Verify latest captured notification

```bash
curl "https://fullstackpm.tech/api/options-intel/notifications/latest" \
  -H "X-Options-Intel-Token: $OPTIONS_INTEL_WEBHOOK_TOKEN"
```

## Deploy checklist

1. Generate a strong random token locally:

   ```bash
   python - <<'PY'
   import secrets
   print(secrets.token_urlsafe(32))
   PY
   ```

2. Add it to the fullstackpm.tech hosting environment as:

   ```text
   OPTIONS_INTEL_WEBHOOK_TOKEN=<generated-token>
   ```

3. Configure options-intel Phase 6 notify code to send:

   ```text
   notify_webhook_url=https://fullstackpm.tech/api/options-intel/notify
   X-Options-Intel-Token=<same generated token>
   ```

Do not commit the token. Gremlins love committed tokens.

Stripe API Keys
Stripe authenticates API requests using your account's API keys. If a request doesn't include a valid key, Stripe returns an invalid request error. A deleted or expired key returns an authentication error.
Key types

Restricted API key (rk*...): permissions you control; limits damage if leaked. Not safe to expose.
Publishable API key (pk*...): safe for front-end code or distributed applications. Safe to expose.
Secret API key (sk*...): unrestricted permissions on all Stripe APIs. Not safe to expose.
Organization API key (sk_org*...): works at the organization level across multiple accounts. Not safe to expose.

Sandbox vs. live mode
All API requests occur in either sandbox (test) or live mode. Test keys start with pk*test*, rk*test*, and sk*test* — card networks don't process real payments. Live keys start with pk*live*, rk*live*, and sk*live*. Each mode has its own set of keys, and objects in one mode aren't accessible to the other.
Protecting your keys
Only publishable keys are safe to expose outside your backend. Best practices: store sensitive keys in a secrets vault (or environment variables if a vault isn't available); never put keys in source code or config files checked into version control; configure access policies so keys can only be used from known servers; rotate keys when team members with access leave; and never share keys over email, chat, or unencrypted channels.
Rotating a key
Rotating revokes an old key and generates a replacement. Both the old and new keys keep working for up to 7 days so you can migrate across your servers without downtime, then the old key expires.

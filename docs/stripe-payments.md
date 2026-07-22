Online Payments with Stripe
Stripe provides a suite of tools for accepting payments online, including the Optimized Checkout Suite: prebuilt payment UIs, dynamic payment methods, and Link for faster checkout.
Integration options

Shareable Payment Links (no code): share a link to a Stripe payment page without a website.
Full Page (recommended): embed or redirect to a prebuilt payment page on your website.
Embedded Form: embed a prebuilt payment form directly on your website.
Custom Payment Flow: use Stripe Elements to design a custom payment collection page.
In-app Payments: accept payments in iOS, Android, or React Native apps using the Mobile Payment Element.

Choosing your API
Stripe recommends the Checkout Sessions API for most integrations — it builds both basic and complex checkout flows with far less code. Use the Payment Intents API when you need complete control over checkout state and custom logic for discounts, tax, subscriptions, or currency conversion (more code, more maintenance).
Checkout Sessions has built-in tax calculation, subscriptions, discounts, shipping, address collection, order tracking, and automatic 24-hour session expiration. Payment Intents requires manual handling of most of these.
The Payment Intents API
The Payment Intents API handles complex payment flows with a status that changes over the PaymentIntent's lifecycle. It tracks a payment from creation through checkout and triggers additional authentication steps (like Strong Customer Authentication) when required. Advantages include automatic authentication handling, no double charges, and no idempotency-key issues.
What is a PaymentIntent?
A PaymentIntent encapsulates details about a transaction: the supported payment methods, the amount to collect, and the desired currency. Each PaymentIntent typically correlates with a single shopping cart or customer session.
To create one, specify the amount and currency (e.g. amount=1099, currency=usd). Best practices: create it early (as soon as you know the amount), reuse the same PaymentIntent if checkout is interrupted and resumes, and use idempotency keys to prevent duplicates.
The client secret
The PaymentIntent contains a client secret — a unique key that lets the client side securely access fields like status, amount, and currency while hiding sensitive ones. Don't log the client secret, embed it in URLs, or expose it to anyone other than the customer, and ensure TLS is enabled on any page that includes it.
After the payment
A PaymentIntent may have more than one Charge object if there were multiple attempts (for example, retries). It's best practice for your server to monitor webhooks to detect when a payment succeeds or fails. Don't store sensitive information (PII, card details) in metadata or the description field.

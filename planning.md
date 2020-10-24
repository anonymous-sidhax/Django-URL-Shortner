### Changes Required
- Beautify Copy Button on index.html
- Don't reload the page on shorten button click - instead just reload the form and show the shorten link without reloading the whole page.
- Remove Success or Error Messages after 5 seconds - (messages.success(request, "message"))

### Requirements:
- Ads
- Setting password for links
- Browser Extension
- multiple countries
- https
- QR Code Support [future]

- Links will expire after a standard default timespan. Users should be able to specify the expiration time.
- How do we detect and prevent abuse? A malicious user can put us out of business by consuming all URL keys in the current design. To prevent abuse, we can limit users via their api_dev_key. Each api_dev_key can be limited to a certain number of URL creations and redirections per some time period (which may be set to a different duration per developer key).

### Non-Functional Requirements:
- The system should be highly available. This is required because, if our service is down, all the URL redirections will start failing.
- URL redirection should happen in real-time with minimal latency.

### Extended Requirements:
- Analytics; e.g., how many times a redirection happened?
- Our service should also be accessible through REST APIs by other services.

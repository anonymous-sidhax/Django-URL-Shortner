### Requirements:
- Ads
- Setting password for links
- Browser Extension
- multiple countries
- https

- Links will expire after a standard default timespan. Users should be able to specify the expiration time.
- How do we detect and prevent abuse? A malicious user can put us out of business by consuming all URL keys in the current design. To prevent abuse, we can limit users via their api_dev_key. Each api_dev_key can be limited to a certain number of URL creations and redirections per some time period (which may be set to a different duration per developer key).

### Non-Functional Requirements:
- The system should be highly available. This is required because, if our service is down, all the URL redirections will start failing.
- URL redirection should happen in real-time with minimal latency.

### Extended Requirements:
- Analytics; e.g., how many times a redirection happened?
- Our service should also be accessible through REST APIs by other services.

### API:
We can have SOAP or REST APIs to expose the functionality of our service. Following could be the definitions of the APIs for creating and deleting URLs:

- createURL(api_dev_key, original_url, custom_alias=None, user_name=None, expire_date=None)

### Parameters:
- api_dev_key (string): The API developer key of a registered account. This will be used to, among other things, throttle users based on their allocated quota.
- original_url (string): Original URL to be shortened.
- custom_alias (string): Optional custom key for the URL.
- user_name (string): Optional user name to be used in encoding.
- expire_date (string): Optional expiration date for the shortened URL.
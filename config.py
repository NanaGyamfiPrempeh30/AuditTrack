# config.py - Application configuration

import os

# Database settings
DATABASE_URL = "postgresql://admin:password123@localhost:5432/myapp"

# AWS Credentials (TODO: move to environment variables)
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"

# API Keys
STRIPE_SECRET_KEY = "sk_live_51H7xKLExample1234567890abcdefghijklmnop"
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Application settings
DEBUG = True
SECRET_KEY = "super-secret-key-do-not-share-1234567890"
```

This contains multiple security issues:
- Hardcoded AWS credentials
- Database password in connection string
- Stripe API key
- GitHub token
- Debug mode enabled
- Hardcoded secret key

---

### **Test 2: Exposed PEM Key**

Create a file called `server-key.pem`:
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MbPMBWAEkRMWzng2
TGvXwDwMYDb7EXAMPLE0000000000000000000000000000000000000000000000
00000000000000000000EXAMPLE000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000EXAM
PLEAAAAAAAAAAAAAAAAAAAAAbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
-----END RSA PRIVATE KEY-----

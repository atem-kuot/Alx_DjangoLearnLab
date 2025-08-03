### Authentication Setup:
- We use Token Authentication via DRF.
- Obtain token at: `/api/auth-token/` by sending `username` and `password`.
- Include token in header for all API requests:
  `Authorization: Token <your-token>`

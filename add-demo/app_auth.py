import os

mcp = FastMCP("My App",
        auth_server_provider=MyOAuthServerProvider(),
        auth=AuthSettings(
            issuer_url=os.getenv("ISSUER_URL", "https://myapp.com"),
            revocation_options=RevocationOptions(
                enabled=True,
            ),
            client_registration_options=ClientRegistrationOptions(
                enabled=True,
                valid_scopes=["myscope", "myotherscope"],
                default_scopes=["myscope"],
            ),
            required_scopes=["myscope"],
        ),
)
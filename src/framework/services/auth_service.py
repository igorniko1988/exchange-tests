from framework.services.base_service import BaseService


class AuthService(BaseService):
    def register(self, email, password):
        data = {"email": email, "password": password}
        return self.client.post("/auth/register", json=data)

    def login(self, email, password):
        data = {"email": email, "password": password}
        return self.client.post("/auth/login", json=data)

    def me(self):
        return self.client.get("/me")

    def update_me(self, display_name: str | None = None, **extra):
        body = {}
        if display_name is not None:
            body["display_name"] = display_name
        body.update(extra)
        return self.client.patch("/me", json=body)

    def refresh_token(self, token):
        return self.client.post("/auth/refresh", json={"refresh_token": token})

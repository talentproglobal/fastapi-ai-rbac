from oso import Oso

oso = Oso()

roles_permissions = {
    "admin": ["read", "write", "delete"],
    "user": ["read", "write"]
}

def setup_permissions():
    for role, permissions in roles_permissions.items():
        for perm in permissions:
            oso.policy(f"allow({role}, {perm});")

setup_permissions()

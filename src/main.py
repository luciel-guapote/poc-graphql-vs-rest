import strawberry
from flask import Flask, jsonify
from strawberry.flask.views import GraphQLView

# --- BASE DE DATOS DE PRUEBA ---
USUARIOS_DB = {
    "1": {
        "id": "1",
        "nombre": "Kenya Jiménez",
        "email": "lucielguapote26@gmail.com",
        "rol": "Desarrolladora",
        "detalles_privados": "Información sensible de servidor",
    },
    "2": {
        "id": "2",
        "nombre": "Ramses Lopez",
        "email": "capitanramenaso@gmail.com",
        "rol": "Administrador",
        "detalles_privados": "Información sensible de servidor",
    },
}

app = Flask(__name__)

# ==========================================
# 1. ENFOQUE REST API
# ==========================================
# REST devuelve TODOS los datos del usuario (Over-fetching)
@app.route("/api/rest/usuario/<id_usuario>", methods=["GET"])
def get_usuario_rest(id_usuario):
    usuario = USUARIOS_DB.get(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario)


# ==========================================
# 2. ENFOQUE GRAPHQL
# ==========================================
# GraphQL permite al cliente pedir SOLO los campos que necesita
@strawberry.type
class UsuarioGraphQL:
    id: str
    nombre: str
    email: str
    rol: str

@strawberry.type
class Query:
    @strawberry.field
    def usuario(self, id: str) -> UsuarioGraphQL:
        u = USUARIOS_DB.get(id)
        if not u:
            return None
        return UsuarioGraphQL(
            id=u["id"],
            nombre=u["nombre"],
            email=u["email"],
            rol=u["rol"]
        )

schema = strawberry.Schema(query=Query)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

if __name__ == "__main__":
    print("==================================================")
    print("Servidor PoC: GraphQL vs REST APIs")
    print("Endpoint REST:    http://127.0.0.1:5000/api/rest/usuario/1")
    print("Endpoint GraphQL: http://127.0.0.1:5000/graphql")
    print("==================================================")
    app.run(port=5000, debug=True)
# Actualización de pruebas GraphQL

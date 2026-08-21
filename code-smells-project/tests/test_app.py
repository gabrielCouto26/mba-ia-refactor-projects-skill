import unittest
import os
import json
from app import create_app
from config import Config
from database import get_db

class TestConfig(Config):
    TESTING = True
    DATABASE_PATH = "test_loja.db"
    DEBUG = False
    ADMIN_USERNAME = "test-admin"
    ADMIN_PASSWORD = "test-admin-password"

class AppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Reset DB before test
        with self.app.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM itens_pedido")
            cursor.execute("DELETE FROM pedidos")
            cursor.execute("DELETE FROM produtos")
            cursor.execute("DELETE FROM usuarios")
            db.commit()
            
            # Seed test data
            cursor.execute("INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES ('Prod A', 'Desc A', 100.0, 10, 'informatica')")
            cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES ('User Test', 'test@email.com', 'secret', 'cliente')")
            db.commit()

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TestConfig.DATABASE_PATH):
            os.remove(TestConfig.DATABASE_PATH)

    def test_index_and_health(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("endpoints", res.json)

        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["status"], "ok")
        self.assertEqual(res.json["database"], "connected")

    def test_admin_routes_require_authentication_and_never_execute_sql(self):
        res = self.client.post("/admin/reset-db")
        self.assertEqual(res.status_code, 401)

        res = self.client.post(
            "/admin/reset-db",
            auth=(TestConfig.ADMIN_USERNAME, TestConfig.ADMIN_PASSWORD)
        )
        self.assertEqual(res.status_code, 200)

        res = self.client.post("/admin/query", json={"sql": "SELECT 1"})
        self.assertEqual(res.status_code, 404)

    def test_produtos_crud(self):
        # List
        res = self.client.get("/produtos")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["sucesso"])
        self.assertEqual(len(res.json["dados"]), 1)
        prod_id = res.json["dados"][0]["id"]

        # Get by id
        res = self.client.get(f"/produtos/{prod_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["dados"]["nome"], "Prod A")

        # Create
        res = self.client.post("/produtos", json={
            "nome": "Prod B",
            "descricao": "Desc B",
            "preco": 200.0,
            "estoque": 5,
            "categoria": "moveis"
        })
        self.assertEqual(res.status_code, 201)
        new_id = res.json["dados"]["id"]

        # Update
        res = self.client.put(f"/produtos/{new_id}", json={
            "nome": "Prod B Updated",
            "preco": 250.0,
            "estoque": 4
        })
        self.assertEqual(res.status_code, 200)

        # Search
        res = self.client.get("/produtos/busca?q=Updated")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["total"], 1)

        # Delete
        res = self.client.delete(f"/produtos/{new_id}")
        self.assertEqual(res.status_code, 200)

    def test_usuario_and_login(self):
        # Create user
        res = self.client.post("/usuarios", json={
            "nome": "Novo Usuario",
            "email": "novo@email.com",
            "senha": "password123"
        })
        self.assertEqual(res.status_code, 201)

        # Login success
        res = self.client.post("/login", json={
            "email": "novo@email.com",
            "senha": "password123"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["sucesso"])

        # Login failure
        res = self.client.post("/login", json={
            "email": "novo@email.com",
            "senha": "wrongpassword"
        })
        self.assertEqual(res.status_code, 401)

    def test_pedidos_flow(self):
        # Fetch initial prod & user id
        prod_res = self.client.get("/produtos")
        prod_id = prod_res.json["dados"][0]["id"]

        user_res = self.client.get("/usuarios")
        user_id = user_res.json["dados"][0]["id"]

        # Create Order
        res = self.client.post("/pedidos", json={
            "usuario_id": user_id,
            "itens": [{"produto_id": prod_id, "quantidade": 2}]
        })
        self.assertEqual(res.status_code, 201)
        pedido_id = res.json["dados"]["pedido_id"]

        # List user orders (test N+1 optimized JOIN query)
        res = self.client.get(f"/pedidos/usuario/{user_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["dados"]), 1)
        self.assertEqual(res.json["dados"][0]["itens"][0]["produto_nome"], "Prod A")

        # Update order status
        res = self.client.put(f"/pedidos/{pedido_id}/status", json={"status": "aprovado"})
        self.assertEqual(res.status_code, 200)

    def test_relatorio_vendas(self):
        res = self.client.get("/relatorios/vendas")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json["sucesso"])
        self.assertIn("faturamento_bruto", res.json["dados"])

if __name__ == "__main__":
    unittest.main()

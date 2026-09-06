from app import create_app
def test_login_page():
    app=create_app()
    app.config["TESTING"]=True
    with app.test_client() as c:
        assert c.get("/login").status_code==200

def test_compatibility_api_requires_login():
    app=create_app()
    app.config["TESTING"]=True
    with app.test_client() as c:
        assert c.get("/api/stats").status_code in (302,401)

from app import create_app, db
from app.models import Product

def seed_data():
    app = create_app()
    with app.app_context():
        # Example products
        products = [
            Product(name="Laptop", description="Powerful laptop", price=999.99, stock=10),
            Product(name="Smartphone", description="Latest model", price=599.99, stock=20),
            Product(name="Headphones", description="Noise-cancelling", price=199.99, stock=30)
        ]
        
        # Adding products
        db.session.add_all(products)
        db.session.commit()

        print("Example data added successfully!")

if __name__ == "__main__":
    seed_data()
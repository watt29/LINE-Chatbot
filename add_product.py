import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# --- Firebase Initialization ---
# Make sure your serviceAccountKey.json is in the same directory as this script
cert = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cert,
    {
        "databaseURL": "https://maharat-c35cc-default-rtdb.asia-southeast1.firebasedatabase.app"
    },
)

# --- Helper Functions ---


def get_input(prompt, default=None):
    value = input(prompt)
    return value if value else default


def get_yes_no_input(prompt):
    while True:
        response = input(prompt).lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def get_product_id():
    while True:
        product_id = get_input("Enter Product ID (e.g., 004, 005): ").strip()
        if product_id:
            return product_id
        else:
            print("Product ID cannot be empty.")


def get_image_url():
    while True:
        url = get_input(
            "Enter Image URL (e.g., https://example.com/image.jpg): "
        ).strip()
        if url and (url.startswith("http://") or url.startswith("https://")):
            return url
        else:
            print("Invalid URL. Please enter a valid image URL.")


def get_category(existing_categories_ref):
    existing_categories = existing_categories_ref.get()
    if not existing_categories:
        existing_categories = []

    print("\nAvailable Categories:")
    if existing_categories:
        for i, cat in enumerate(existing_categories):
            print(f"{i+1}. {cat}")
    else:
        print("No categories found. You will create the first one.")

    while True:
        category_input = get_input(
            "Enter Category (select from above or type new): "
        ).strip()
        if category_input:
            if category_input.isdigit() and 1 <= int(category_input) <= len(
                existing_categories
            ):
                return existing_categories[int(category_input) - 1]
            else:
                if category_input not in existing_categories:
                    if get_yes_no_input(
                        f"Category '{category_input}' does not exist. Add it? (y/n): "
                    ):
                        existing_categories.append(category_input)
                        existing_categories_ref.set(existing_categories)
                        print(f"Category '{category_input}' added to knowledge base.")
                        return category_input
                    else:
                        print(
                            "Please choose an existing category or confirm adding a new one."
                        )
                else:
                    return category_input
        else:
            print("Category cannot be empty.")


# --- Main Script ---


def main():
    print("\n--- Add New Product to Firebase ---")

    # Get existing data references
    products_ref = db.reference("products")
    product_details_ref = db.reference("knowledge_base/product_details")
    categories_ref = db.reference("knowledge_base/categories")

    # Get product data
    product_id = get_product_id()
    product_name = get_input("Enter Product Name: ").strip()
    product_image = get_image_url()
    product_description = get_input("Enter Product Description: ").strip()
    product_material = get_input("Enter Product Material: ").strip()
    product_price = get_input("Enter Product Price: ").strip()
    product_category = get_category(categories_ref)

    new_product = {
        "name": product_name,
        "image": product_image,
        "description": product_description,
        "material": product_material,
        "price": product_price,
        "category": product_category,
    }

    # Add product to /products
    products_ref.child(product_id).set(new_product)
    print(f"\nProduct '{product_name}' ({product_id}) added to /products.")

    # Get product details for knowledge base
    if get_yes_no_input(
        "\nDo you want to add detailed info for AI (history, faq)? (y/n): "
    ):
        detail_history = get_input("  Enter History/Background: ").strip()
        detail_authenticity = get_input("  Enter Authenticity Checkpoints: ").strip()

        faqs = []
        print("  Enter FAQs (type 'done' when finished):")
        while True:
            q = get_input("    Question (or 'done'): ").strip()
            if q.lower() == "done":
                break
            a = get_input("    Answer: ").strip()
            if q and a:
                faqs.append({"q": q, "a": a})
            else:
                print("    Question and Answer cannot be empty.")

        new_product_details = {
            "history": detail_history,
            "authenticity_checkpoints": detail_authenticity,
            "faq": faqs,
        }
        product_details_ref.child(product_id).set(new_product_details)
        print(
            f"Detailed info for '{product_name}' ({product_id}) added to knowledge_base/product_details."
        )
    else:
        print("Skipping detailed info for AI.")

    print("\n--- Product addition complete! ---")


if __name__ == "__main__":
    main()

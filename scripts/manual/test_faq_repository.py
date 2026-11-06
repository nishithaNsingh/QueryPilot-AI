from app.repositories.faq_repository import insert_faqs, get_faqs

inserted = insert_faqs()
print("FAQs inserted:", inserted)

print(get_faqs())
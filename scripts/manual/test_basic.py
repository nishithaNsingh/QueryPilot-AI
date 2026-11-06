def test_python_environment():
    assert 1 + 1 == 2


def test_querypilot_test_setup():
    from app.database.connection import get_connection

    connection = get_connection()

    assert connection is not None

    connection.close()


def test_faq_service_import():
    from app.services.faq_service import find_relevant_faq

    assert callable(find_relevant_faq)


def test_order_repository_import():
    from app.repositories.order_repository import get_active_orders

    assert callable(get_active_orders)
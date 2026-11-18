
from sqlmodel import Session, text
from DB.db_config import engine

def test_database():

    try:
        with Session(engine) as session:

            # 1. Start transaction
            with session.begin():

                # 2. Check database connection
                result = session.exec(
                    text("SELECT current_database(), current_user")
                ).first()

                print("Database:", result[0])
                print("User:", result[1])

                # 3. Insert temporary test data
                session.exec(
                    text("""
                        CREATE TEMP TABLE connection_test (
                            id SERIAL PRIMARY KEY,
                            message VARCHAR(100)
                        )
                    """)
                )

                session.exec(
                    text("""
                        INSERT INTO connection_test (message)
                        VALUES ('FastAPI database test successful')
                    """)
                )

                # 4. Read inserted data
                data = session.exec(
                    text("SELECT * FROM connection_test")
                ).all()

                print("Inserted data:", data)

                # 5. Rollback transaction
                raise RuntimeError("ROLLBACK_TEST")

    except RuntimeError as e:
        if str(e) == "ROLLBACK_TEST":
            print("Transaction rolled back successfully!")
        else:
            raise

    except Exception as e:
        print("Database test failed:", e)


if __name__ == "__main__":
    test_database()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config.setting import settings


if settings.stage == "dev":
    engine = create_engine(
        f"postgresql+auroradataapi://:@/{settings.db_name}",
        echo=True,
        connect_args=dict(aurora_cluster_arn=settings.cluster_arn, secret_arn=settings.secret_arn)
    )
else:
    db_url = f"postgresql://" \
             f"{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    engine = create_engine(db_url, echo=True, future=True)

db_session = sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_db_session() -> Session:
    """
    Context manager for database session
    """
    session = db_session()

    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

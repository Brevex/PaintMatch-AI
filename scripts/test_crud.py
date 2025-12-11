import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.crud import crud_paint, crud_user
from app.db.session import SessionLocal
from app.schemas.paint import PaintCreate
from app.schemas.user import UserCreate


def test_crud_operations():
    """
    Executa uma série de testes para as funções CRUD e de segurança.
    """
    print("Iniciando o teste das operações CRUD...")
    db: Session = SessionLocal()

    try:
        print("\n[TESTE] Criando um novo usuário...")
        user_in = UserCreate(
            email="test@example.com",
            password="mytestpassword123",
            full_name="Test User",
        )

        created_user = crud_user.create_user(db, user=user_in)
        print(f"Usuário criado: {created_user.email} (ID: {created_user.id})")
        assert created_user.email == user_in.email
        assert created_user.full_name == user_in.full_name

        print("[TESTE] Verificando se a senha foi hasheada...")
        assert hasattr(created_user, "hashed_password")
        assert created_user.hashed_password != user_in.password
        print("Senha foi hasheada com sucesso.")

        print("[TESTE] Verificando se a senha corresponde ao hash...")
        is_password_correct = verify_password(user_in.password, created_user.hashed_password)
        assert is_password_correct
        print("Verificação de senha bem-sucedida.")

        print(f"[TESTE] Buscando o usuário pelo e-mail: {user_in.email}")
        retrieved_user = crud_user.get_user_by_email(db, email=user_in.email)
        assert retrieved_user
        assert retrieved_user.id == created_user.id
        print("Usuário recuperado com sucesso.")

        print("\n--- Testes de Usuário passaram com sucesso! ---")

        print("\n[TESTE] Criando uma nova tinta...")
        paint_in = PaintCreate(
            name="Suvinil Toque de Seda", color="Branco Neve", finish_type="Acetinado"
        )

        created_paint = crud_paint.create_paint(db, paint=paint_in)
        print(f"Tinta criada: {created_paint.name} (ID: {created_paint.id})")
        assert created_paint.name == paint_in.name
        assert created_paint.color == paint_in.color

        print(f"[TESTE] Buscando a tinta pelo ID: {created_paint.id}")
        retrieved_paint = crud_paint.get_paint(db, paint_id=created_paint.id)
        assert retrieved_paint
        assert retrieved_paint.id == created_paint.id
        print("Tinta recuperada com sucesso.")

        print("\n--- Testes de Tinta passaram com sucesso! ---")

    except AssertionError as e:
        print(f"\n!!!!!! TESTE FALHOU !!!!!!: {e}")
    except Exception as e:
        print(f"\n!!!!!! OCORREU UM ERRO INESPERADO !!!!!!: {e}")
    finally:
        print("\n[INFO] Limpando dados de teste (rollback)...")
        db.rollback()
        db.close()
        print("Sessão do banco de dados fechada.")


if __name__ == "__main__":
    test_crud_operations()

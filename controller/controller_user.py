from fastapi import HTTPException, status
from model import model_user as user_model
from typing import Dict, List, Optional, Any
import mysql.connector
from fastapi.templating import Jinja2Templates

user_model.criar_banco_dados()
user_model.criar_tabela_usuarios()

template = Jinja2Templates(directory="templates")

def criar_usuario(nome: str, email: str, senha: str) -> Dict[str, Any]:
    try:
        user_model.criar_usuario(nome, email, senha)
        return {"nome": nome, "email": email}
    except mysql.connector.Error as e:
        if e.errno == 1062:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

def listar_usuarios() -> List[Dict[str, Any]]:
    try:
        usuarios = user_model.listar_usuarios()
        if not usuarios:
            return []
        return template.TemplateResponse()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar usuários: {str(e)}"
        )

def buscar_usuario(id: int) -> Dict[str, Any]:
    try:
        usuario = user_model.buscar_usuario_por_id(id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar usuário: {str(e)}"
        )

def atualizar_usuario(
    id: int,
    nome: Optional[str] = None,
    email: Optional[str] = None,
    senha: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if nome is not None and len(nome) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome deve ter no mínimo 3 caracteres"
            )

        if senha is not None and len(senha) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A senha deve ter no mínimo 6 caracteres"
            )

        user_model.atualizar_usuario(id, nome, email, senha)
        return buscar_usuario(id)
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        if e.errno == 1062:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

def deletar_usuario(id: int) -> bool:
    try:
        # Primeiro verifica se o usuário existe
        usuario = user_model.buscar_usuario_por_id(id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {id} não encontrado"
            )
        
        # Se existe, deleta
        user_model.deletar_usuario(id)
        return True
    except HTTPException:
        raise
    except mysql.connector.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro inesperado ao deletar usuário: {str(e)}"
        )
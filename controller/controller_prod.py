from fastapi import HTTPException, status, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import model.model_prod as model
from typing import Optional

model.criar_banco_dados()
model.criar_tabela_produtos()

templates = Jinja2Templates(directory="templates")

def criar_produto_page(request: Request):
    return templates.TemplateResponse(
        "produtos/cadastro.html",
        {"request": request}
    )

def criar_produto(request: Request, nome: str, descricao: str, preco: float, estoque: int):
    try:
        validar_produto(nome, descricao, preco, estoque)
        model.criar_produto(nome, descricao, preco, estoque)
        return RedirectResponse(
            url="/produtos",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except HTTPException as e:
        return templates.TemplateResponse(
            "produtos/cadastro.html",
            {
                "request": request,
                "error": e.detail,
                "values": {
                    "nome": nome,
                    "descricao": descricao,
                    "preco": preco,
                    "estoque": estoque
                }
            }
        )

def validar_produto(nome: str, descricao: str, preco: float, estoque: int):
    if len(nome) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O nome deve ter no mínimo 3 caracteres"
        )
    if len(descricao) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A descrição deve ter no mínimo 10 caracteres"
        )
    if preco <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O preço deve ser um valor positivo"
        )
    if estoque < 0 or not isinstance(estoque, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O estoque deve ser um número inteiro maior ou igual a zero"
        )

def listar_produtos(request: Request):
    try:
        produtos = model.listar_produtos()
        return templates.TemplateResponse(
            "produtos/lista.html",
            {"request": request, "produtos": produtos or []}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "produtos/lista.html",
            {
                "request": request,
                "error": f"Erro ao listar produtos: {str(e)}",
                "produtos": []
            }
        )

def obter_produto(id: int):
    try:
        produto = model.obter_produto_por_id(id)
        if produto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não foi encontrado"
            )
        return produto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar produto: {str(e)}"
        )

def atualizar_produto(id: int, nome: Optional[str] = None, descricao: Optional[str] = None,
                    preco: Optional[float] = None, estoque: Optional[int] = None):
    try:
        if nome is not None and len(nome) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O nome deve ter no mínimo 3 caracteres"
            )

        if descricao is not None and len(descricao) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A descrição deve ter no mínimo 10 caracteres"
            )

        if preco is not None and preco <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O preço deve ser um valor positivo"
            )

        if estoque is not None and (estoque < 0 or not isinstance(estoque, int)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O estoque deve ser um número inteiro maior ou igual a zero"
            )

        # Verifica se o produto existe
        produto = model.obter_produto_por_id(id)
        if produto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )

        model.atualizar_produto(id, nome, descricao, preco, estoque)
        return model.obter_produto_por_id(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )

def deletar_produto(id: int):
    try:
        produto = model.obter_produto_por_id(id)
        if produto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado"
            )
        model.deletar_produto(id)
        return {"message": "Produto deletado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )
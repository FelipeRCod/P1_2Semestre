from fastapi import APIRouter, Request, Path, HTTPException, status
from fastapi.responses import RedirectResponse
from controller import controller_prod as produto_controller
from typing import Dict, Any
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/produtos" , tags=["Produtos"])

templates = Jinja2Templates(directory="templates")

@router.get("/")
def listar_produtos(request: Request):
    try:
        return produto_controller.listar_produtos(request)
    except Exception as e:
        return templates.TemplateResponse(
            "produtos/lista.html", {
                "request": request,
                "error": f"Erro ao listar produtos: {str(e)}",
                "produtos": []
            }
        )
@router.get("/cadastro")
async def pagina_cadastro(request: Request):
    return templates.TemplateResponse(
        "produtos/cadastro.html",
        {"request": request}
    )

@router.post("/cadastro")
async def criar_produto(request: Request):
    try:
        form = await request.form()
        produto_controller.criar_produto(
            request = request,
            nome = form["nome"],
            descricao = form["descricao"],
            preco = float(form["preco"]),
            estoque = int(form["estoque"])
        )
        return RedirectResponse(
            url="/produtos",
            status_code = status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        return templates.TemplateResponse(
            "produtos/cadastro.html",{
                "request": request,
                "error": str(e),
                "values": {
                    "nome": form.get("nome", ""),
                    "descricao": form.get("descricao", ""),
                    "preco": form.get("preco", ""),
                    "estoque": form.get("estoque", "")
                }
            }
        )

@router.get("/{id}")
def obter_produto(id: int = Path(..., gt=0)):
    try:
        produto = produto_controller.obter_produto(id)
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produto com ID {id} não encontrado"
            )
        return produto
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter produto"
        )



@router.put("/{id}")
async def atualizar_produto(request: Request, id: int = Path(..., gt=0)):
    try:
        form = await request.form()

        dados_atualizacao: Dict[str, Any] = {}

        if "nome" in form:
            dados_atualizacao["nome"] = form["nome"]

        if "descricao" in form:
            dados_atualizacao["descricao"] = form["descricao"]

        if "preco" in form:
            try:
                dados_atualizacao["preco"] = float(form["preco"])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O preço deve ser um número válido"
                )

        if "estoque" in form:
            try:
                dados_atualizacao["estoque"] = int(form["estoque"])
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="O estoque deve ser um número inteiro"
                )

        if not dados_atualizacao:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo fornecido para atualização"
            )

        return produto_controller.atualizar_produto(
            id=id,
            nome=dados_atualizacao.get("nome"),
            descricao=dados_atualizacao.get("descricao"),
            preco=dados_atualizacao.get("preco"),
            estoque=dados_atualizacao.get("estoque")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )

@router.delete("/{id}")
def deletar_produto(request: Request, id: int
                    = Path(..., gt=0)):
    try:
        produto_controller.deletar_produto(id)
        return {"message": "Produto excluído com sucesso"}
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar produto: {str(e)}"
        )
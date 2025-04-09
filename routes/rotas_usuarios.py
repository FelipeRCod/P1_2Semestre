from fastapi import APIRouter, Request, HTTPException, status, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from controller import controller_user
from typing import Dict, Any, Union, List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=Dict[str, Any])
def listar():
    try:
        usuarios: List[Dict[str, Any]] = controller_user.listar_usuarios()
        return {"usuarios": usuarios}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar usuários: {str(e)}"
        )

@router.post("/usuarios", response_model=Dict[str, Any])
async def criar(request: Request):
    try:
        form = await request.form()
        dados_usuario: Dict[str, Any] = {
            "nome": form["nome"],
            "email": form["email"],
            "senha": form["senha"]
        }
        
        required_fields = ["nome", "email", "senha"]
        for field in required_fields:
            if field not in form:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Campo '{field}' é obrigatório"
                )
        
        usuario_criado = await controller_user.criar_usuario(**dados_usuario)
        return {"message": "Usuário criado com sucesso", "usuario": usuario_criado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

@router.delete("/delete/{user_id}", response_model=Dict[str, str])
async def deletar(user_id: int):
    try:
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID do usuário não fornecido"
            )
        
        result = controller_user.deletar_usuario(user_id)
        if result:
            return {"message": f"Usuário {user_id} deletado com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )

@router.get("/usuarios/edit/{user_id}", response_model=Dict[str, Any])
def editar(request: Request, user_id: int = Path(..., gt=0)):
    try:
        usuario: Dict[str, Any] = controller_user.buscar_usuario(user_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao preparar edição do usuário: {str(e)}"
        )

@router.post("/usuarios/update/{user_id}", response_model=Dict[str, Any])
async def atualizar(request: Request, user_id: int = Path(..., gt=0)):
    try:
        form = await request.form()
        dados_atualizacao: Dict[str, Any] = {
            "nome": form.get("nome"),
            "email": form.get("email")
        }
        
        usuario_atualizado = controller_user.atualizar_usuario(user_id, **dados_atualizacao)
        return {"message": "Usuário atualizado com sucesso", "usuario": usuario_atualizado}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar usuário: {str(e)}"
        )

@router.get("/usuarios/lista")
async def listar_usuarios(request: Request):
    usuarios = controller_user.listar_usuarios()
    return templates.TemplateResponse(
        "usuarios/lista_usuario.html",
        {"request": request, "usuarios": usuarios}
    )

@router.get("/usuarios/editar")
async def render_editar(request: Request):
    try:
        return templates.TemplateResponse(
            "usuarios/editar_usuario.html",
            {"request": request}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao renderizar página de edição: {str(e)}"
        )

@router.get("/usuarios/cadastro")
async def render_cadastro(request: Request):
    return templates.TemplateResponse(
        "usuarios/cadastro_usuario.html",
        {"request": request}
    )

@router.get("/usuarios")
async def listar_usuarios_page(request: Request):
    return templates.TemplateResponse(
        "usuarios/lista_usuario.html",
        {"request": request}
    )



from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi import status
from fastapi.exceptions import HTTPException

from _app.core.configs import settings
from _app.core.auth import set_auth, unset_auth
from _app.controllers.membro_controller import MembroController
from _app.core.deps import valida_login

router = APIRouter()



@router.get('/', name='index')
async def index(request: Request) -> Response:
    context = await valida_login(request)
    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('login.html', context=context)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('login.html', context=context)
    
    return RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)


@router.get('/register', name='get_register')
async def get_login(request: Request) -> Response:
    context = await valida_login(request)
    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('register.html', context=context)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('register.html', context=context)
    
    return RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)



@router.post('/login', name='post_login')
async def post_login(request: Request) -> Response:
    membro_controller: MembroController = MembroController(request)

    # Receber dados do form
    form = await request.form()
    email: str = form.get('email')
    senha: str = form.get('senha')

    membro = await membro_controller.login_membro(email=email, senha=senha)

    if not membro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)

    # Adiciona o cookie na response
    set_auth(response=response, membro_id=membro.id)

    return response


@router.get('/login', name='get_login')
async def get_login(request: Request) -> Response:
    context = await valida_login(request)
    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('login.html', context=context)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('login.html', context=context)
    
    return RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)

@router.get('/register', name='get_register')
async def get_login(request: Request) -> Response:
    context = await valida_login(request)
    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('register.html', context=context)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('register.html', context=context)
    
    return RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)


@router.post('/register', name='post_register')
async def post_register(request: Request) -> Response:
    context = {'request': request}
    membro_controller = MembroController(request)

    # Receber dados do form
    form = await request.form()
    nome = form.get('nome')
    email = form.get('email')
    senha = form.get('senha')
    funcao = "inscrito" if email != 'example@safe_email.com' else 'administrador'

    form_data = {
        "nome": nome,
        "funcao": funcao,
        "email": email,
        "senha": senha
    }

    try:
        await membro_controller.post_register(dados=form_data)
    except ValueError as err:
        context.update({"error": err, "objeto": form_data})
        return settings.TEMPLATES.TemplateResponse("admin/membro/create.html", context=context)

    membro = await membro_controller.login_membro(email=email, senha=senha)

    if not membro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = RedirectResponse(request.url_for('admin_index'), status_code=status.HTTP_302_FOUND)
    
    # Adiciona o cookie na response
    set_auth(response=response, membro_id=membro.id)

    return response


@router.get('/logout', name='logout')
async def logout(request: Request) -> Response:
    response = RedirectResponse(request.url_for('index'), status_code=status.HTTP_302_FOUND)

    unset_auth(response=response)

    return response
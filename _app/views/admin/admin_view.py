from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import status

from _app.core.configs import settings
from _app.views.admin.membro_admin import membro_admin

from _app.core.deps import valida_login

router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router)


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    context = await valida_login(request)

    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    
    if context['membro'].funcao == "administrador":
        return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)

    elif context['membro'].funcao == "inscrito":
        return settings.TEMPLATES.TemplateResponse('inscrito/index.html', context=context)

    elif context['membro'].funcao == "inscrito_1":
        return settings.TEMPLATES.TemplateResponse('inscrito_1/index.html', context=context)




import uvicorn

from implementation.settings import setting

uvicorn.run(
    'implementation.app:app',
    host= setting.server_hosr,
    port= setting.server_post,
    reload=True
)
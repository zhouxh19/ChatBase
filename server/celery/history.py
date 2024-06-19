import urllib

from server.knowledge_base.utils import validate_kb_name
from server.utils import BaseResponse
from celery_app import app

def kb_upload_active_tasks( knowledge_base_name: str) -> BaseResponse:
    if not validate_kb_name(knowledge_base_name):
        return BaseResponse(code=403, msg="Don't attack me", data=[])
    knowledge_base_name = urllib.parse.unquote(knowledge_base_name)
    inspect = app.control.inspect()
    # 获取所有正在执行的任务
    active_tasks = inspect.active()
    # 打印每个worker的活跃任务
    kb_task_data = []
    if not active_tasks:
        return BaseResponse(code=200, msg="success", data=[])
    for worker, tasks in active_tasks.items():
        for task in tasks:
            if task['name'] == 'upload_docs':
                if task['args'][1] == knowledge_base_name:
                    kb_task_data.append(task)
    return BaseResponse(code=200, msg="success", data=kb_task_data)











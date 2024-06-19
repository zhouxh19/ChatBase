from typing import List
from configs import DEFAULT_VS_TYPES, logger, log_verbose
from server.knowledge_base.kb_service.base import KBServiceFactory
from celery_app import app
from server.knowledge_base.utils import KnowledgeFile, files2docs_in_thread


@app.task(name='upload_docs')
def celery_upload_docs(file_names: List[str], knowledge_base_name: str, chunk_size: int,
                       chunk_overlap: int, zh_title_enhance: bool,
                       not_refresh_vs_cache: bool):
    failed_files = {}
    kb_files = []
    # 生成需要加载docs的文件列表
    for file_name in file_names:
        try:
            kb_files.append(KnowledgeFile(filename=file_name, knowledge_base_name=knowledge_base_name))
        except Exception as e:
            msg = f"加载文档 {file_name} 时出错：{e}"
            logger.error(f'{e.__class__.__name__}: {msg}',
                         exc_info=e if log_verbose else None)
            failed_files[file_name] = msg


    for vs_type in DEFAULT_VS_TYPES:
        kb = KBServiceFactory.get_service(knowledge_base_name, vs_type)
        if kb is None:
            continue

        # 从文件生成docs，并进行向量化。
        # 这里利用了KnowledgeFile的缓存功能，在多线程中加载Document，然后传给KnowledgeFile
        for status, result in files2docs_in_thread(kb_files,
                                                   chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap,
                                                   zh_title_enhance=zh_title_enhance):
            if status:
                kb_name, file_name, new_docs = result
                kb_file = KnowledgeFile(filename=file_name,
                                        knowledge_base_name=knowledge_base_name)
                kb_file.splited_docs = new_docs
                kb.update_doc(kb_file, not_refresh_vs_cache=True)
            else:
                kb_name, file_name, error = result
                failed_files[file_name] = error

        if not not_refresh_vs_cache:
            kb.save_vector_store()

    return True

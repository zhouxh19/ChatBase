import os

from configs import CHUNK_SIZE, OVERLAP_SIZE, ZH_TITLE_ENHANCE, DEFAULT_VS_TYPES
from server.knowledge_base.kb_doc_api import update_docs
from server.knowledge_base.kb_service.base import KBServiceFactory


def save_files_to_vs(
        file_names: [str],
        knowledge_base_name: str,
        to_vector_store: bool = True,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = OVERLAP_SIZE,
        zh_title_enhance: bool = ZH_TITLE_ENHANCE):

    failed_files = {}

    # 对保存的文件进行向量化
    if to_vector_store:
        for vs_type in DEFAULT_VS_TYPES:
            kb = KBServiceFactory.get_service(knowledge_base_name, vs_type)
            if kb is None:
                continue

            result = update_docs(
                knowledge_base_name=knowledge_base_name,
                file_names=file_names,
                override_custom_docs=True,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                zh_title_enhance=zh_title_enhance,
                docs={},
                not_refresh_vs_cache=True,
            )
            failed_files.update(result.data["failed_files"])
            kb.save_vector_store()

if __name__ == '__main__':
    files = [
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-0.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-2000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-4000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-6000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-8000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-10000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-12000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-14000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-16000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-18000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-20000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-22000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-24000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-26000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-28000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-30000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-32000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-34000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-36000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-38000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-40000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-42000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-44000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-46000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-48000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-50000.json",
        "/home/ecs-user/Data-chat/knowledge_base/db-qa/content/DBstackOverflow-52000.json",
    ]
    save_files_to_vs(files, "db-qa")


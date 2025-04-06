"""
@Time ： 2025-04-05
@Auth ： Adam Lyu
"""
import pkgutil
import inspect
import importlib
from pathlib import Path
from beanie import Document


def get_all_document_models() -> list[type[Document]]:
    """
    自动收集 app.models 包中所有 Beanie Document 子类。
    """
    document_models = []
    package_dir = Path(__file__).resolve().parent
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, Document) and obj is not Document:
                document_models.append(obj)

    return document_models

import os

from pathlib import Path
import argparse
import shutil


_API_TEMPLATE = """
from fastapi import APIRouter, Request


from app.api.group.logic import logic

r = APIRouter()


@r.get("/list")
async def get_list(req: Request):
    return await logic.get_list(req=req)

"""

ProjectDirectory = "universal-template"


def _init_project(name) -> None:
    print(">>> wait cloned project")
    os.system(
        "git clone git@gitlab.i.mosynx.com:paas/service-template/universal-template.git"
    )

    git_folder_path = os.path.join(ProjectDirectory, ".git")
    # 检查.git文件夹是否存在
    if os.path.exists(git_folder_path) and os.path.isdir(git_folder_path):
        try:
            # 使用递归方式删除整个.git文件夹及其内容
            shutil.rmtree(git_folder_path)
        except Exception as e:
            print(f"Failed to remove the .git folder: {e}")

    old_dir_path = os.path.join(os.getcwd(), ProjectDirectory)
    new_dir_path = os.path.join(os.getcwd(), name)
    os.rename(old_dir_path, new_dir_path)


class Api:

    def __init__(self, name: str) -> None:
        self._name: str = name
        self._destination: Path = Path.cwd()

    def generated_dirs(self) -> None:
        print(">>> wait generate necessary directory")

        api_directory: Path = self._destination / "api"

        # 判断当前目录下是否有api文件夹
        if not api_directory.exists():
            raise FileNotFoundError("api directory not found")

        router_directory: Path = api_directory / self._name
        router_version1_directory: Path = router_directory / "v1"
        router_crud_directory: Path = router_directory / "crud"
        router_logic_directory: Path = router_directory / "logic"
        router_model_directory: Path = router_directory / "model"

        # 定义api文件路径
        self._api_file_path: Path = router_version1_directory / "api.py"

        # 在api文件夹内创建必要目录
        router_directory.mkdir()
        router_version1_directory.mkdir()
        router_crud_directory.mkdir()
        router_logic_directory.mkdir()
        router_model_directory.mkdir()

        print("done!")

    def generated_api_file(self) -> None:
        print(">>> wait generate api file")

        if hasattr(self, "_api_file_path"):
            with open(self._api_file_path, "w") as new_file:
                new_file.write(_API_TEMPLATE)
            print("done!")
        else:
            print("write the api file. u need to manually create the file")

    def do(self) -> None:
        self.generated_dirs()
        self.generated_api_file()


def _run(args) -> None:
    if args.operation == "init":
        # 执行init操作的逻辑
        _init_project(args.name)
    elif args.operation == "api":
        # 执行api操作的逻辑
        obj = Api(args.name)
        obj.do()


def main() -> None:
    parser = argparse.ArgumentParser(description="✨FastAPI Fast generatora✨")
    subparsers = parser.add_subparsers(dest="operation")

    # 初始化项目
    init_parser = subparsers.add_parser("init", help="initialize project")
    init_parser.add_argument("name", type=str, help="project name")

    # 生成路由组
    api_parser = subparsers.add_parser("api", help="generate route group")
    api_parser.add_argument("name", type=str, help="route group name")

    _run(parser.parse_args())


if __name__ == "__main__":
    main()

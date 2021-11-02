
import subprocess
from typing import Any, Dict, List

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.apps.filesystem.services import workingdir_service
from logic.libs.logger.logger import logger

_NAME_FILE_TO_EXECUTE = 'module.py'
_NAME_FILE_LOGS = 'logs.log'

_WORKS_NAME_RUNNED = []


def start(id: str, files_bytes_dict: Dict[str, bytes]):

    logger().info(f'Generando workingdir -> proceso: {id}')
    workingdir_service.create_by_id(id)

    base_path = workingdir_service.fullpath(id)

    for file_name, file_bytes in files_bytes_dict.items():

        logger().info(f'Generando archivo -> {file_name}')

        with open(f'{base_path}/{file_name}', 'w') as f:
            f.write(file_bytes.decode())

    _exec(id)
    _WORKS_NAME_RUNNED.append(id)


def _exec(id: str):

    base_path = workingdir_service.fullpath(id)

    cmd = f'cd {base_path} && python3 {_NAME_FILE_TO_EXECUTE} > {_NAME_FILE_LOGS}'

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

    _notify_work_end(id)


def get_logs(id: str) -> str:

    path = workingdir_service.fullpath(id) + f'/{_NAME_FILE_LOGS}'
    with open(path, 'r') as f:
        return f.read()


def list_all_running() -> List[str]:
    return _WORKS_NAME_RUNNED


def delete(id: str):
    global _WORKS_NAME_RUNNED
    _WORKS_NAME_RUNNED.remove(id)


def _notify_work_end(id: str):

    url = get_var(Vars.JAIME_URL) + f'/api/v1/works/{id}/finish'
    requests.patch(url, timeout=5, verify=False)

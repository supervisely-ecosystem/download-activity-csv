# This module contains the functions that are used to configure the input and output of the workflow for the current app.

from typing import Union

import supervisely as sly


def workflow_input(api: sly.Api, project_id: Union[int, str]):
    api.app.workflow.add_input_project(int(project_id))
    sly.logger.debug(f"Workflow: Input project - {project_id}")


def workflow_output(api: sly.Api, file: Union[int, sly.api.file_api.FileInfo]):
    try:
        if isinstance(file, int):
            file = api.file.get_info_by_id(file)
        relation_settings = sly.WorkflowSettings(
            url=f"/files/{file.id}/true/?teamId={file.team_id}",
            url_title="Download CSV",
        )
        meta = sly.WorkflowMeta(relation_settings=relation_settings)
        api.app.workflow.add_output_file(file, meta=meta)
        sly.logger.debug(f"Workflow: Output file - {file}")
    except Exception as e:
        sly.logger.debug(f"Failed to add output to the workflow: {repr(e)}")

#  coding=utf-8
#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

import httpx

from argilla.client.sdk.client import AuthenticatedClient
from argilla.client.sdk.commons.errors_handler import handle_response_error
from argilla.client.sdk.commons.models import (
    ErrorMessage,
    HTTPValidationError,
    Response,
)
from argilla.client.sdk.datasets.v1.models import (
    FeedbackDatasetModel,
    FeedbackRecordsModel,
)


def create_dataset(
    client: AuthenticatedClient,
    name: str,
    workspace_id: str,
    guidelines: Optional[str] = None,
) -> Response[Union[FeedbackDatasetModel, ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets".format(client.base_url)

    body = {"name": name, "workspace_id": workspace_id}
    if guidelines is not None:
        body.update({"guidelines": guidelines})

    response = httpx.post(
        url=url,
        json=body,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 201:
        parsed_response = FeedbackDatasetModel(**response.json())
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=parsed_response,
        )
    return handle_response_error(response)


@lru_cache(maxsize=None)
def get_dataset(
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[FeedbackDatasetModel, ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}".format(client.base_url, id=id)

    response = httpx.get(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        parsed_response = FeedbackDatasetModel(**response.json())
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=parsed_response,
        )
    return handle_response_error(response)


def delete_dataset(
    client: AuthenticatedClient,
    id: str,
) -> Response:
    url = "{}/api/v1/datasets/{id}".format(client.base_url, id=id)

    response = httpx.delete(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
        )
    return handle_response_error(response)


def publish_dataset(
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[FeedbackDatasetModel, ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}/publish".format(client.base_url, id=id)

    response = httpx.put(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        parsed_response = FeedbackDatasetModel(**response.json())
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=parsed_response,
        )
    return handle_response_error(response)


def list_datasets(
    client: AuthenticatedClient,
) -> Response[Union[List[FeedbackDatasetModel], ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/me/datasets".format(client.base_url)

    response = httpx.get(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        parsed_response = [FeedbackDatasetModel(**dataset) for dataset in response.json()["items"]]
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=parsed_response,
        )
    return handle_response_error(response)


def get_records(
    client: AuthenticatedClient,
    id: str,
    offset: int = 0,
    limit: int = 50,
) -> Response[Union[FeedbackRecordsModel, ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/me/datasets/{id}/records".format(client.base_url, id=id)

    response = httpx.get(
        url=url,
        params={"include": "responses", "offset": offset, "limit": limit},
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        parsed_response = FeedbackRecordsModel(**response.json())
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=parsed_response,
        )
    return handle_response_error(response)


def add_record(
    client: AuthenticatedClient,
    id: str,
    record: Dict[str, Any],
) -> Response:
    url = "{}/api/v1/datasets/{id}/records".format(client.base_url, id=id)

    response = httpx.post(
        url=url,
        json={"items": [record]},
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 204:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
        )
    return handle_response_error(response)


def get_fields(
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[List[Dict[str, Any]], ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}/fields".format(client.base_url, id=id)

    response = httpx.get(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=response.json()["items"],
        )
    return handle_response_error(response)


def add_field(
    client: AuthenticatedClient,
    id: str,
    field: Dict[str, Any],
) -> Response[Union[ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}/fields".format(client.base_url, id=id)

    response = httpx.post(
        url=url,
        json=field,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 201:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
        )
    return handle_response_error(response)


def get_questions(
    client: AuthenticatedClient,
    id: str,
) -> Response[Union[List[Dict[str, Any]], ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}/questions".format(client.base_url, id=id)

    response = httpx.get(
        url=url,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 200:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
            parsed=response.json()["items"],
        )
    return handle_response_error(response)


def add_question(
    client: AuthenticatedClient,
    id: str,
    question: Dict[str, Any],
) -> Response[Union[ErrorMessage, HTTPValidationError]]:
    url = "{}/api/v1/datasets/{id}/questions".format(client.base_url, id=id)

    response = httpx.post(
        url=url,
        json=question,
        headers=client.get_headers(),
        cookies=client.get_cookies(),
        timeout=client.get_timeout(),
    )

    if response.status_code == 201:
        return Response(
            status_code=response.status_code,
            content=response.content,
            headers=response.headers,
        )
    return handle_response_error(response)

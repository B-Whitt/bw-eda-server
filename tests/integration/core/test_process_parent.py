#  Copyright 2023 Red Hat, Inc.
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


import pytest
from pytest_lazyfixture import lazy_fixture

from aap_eda.core import models
from aap_eda.core.enums import ActivationRequest, ActivationStatus


@pytest.mark.parametrize(
    "instance",
    [
        pytest.param(
            lazy_fixture("new_activation"),
            id="activation",
        ),
    ],
)
@pytest.mark.django_db
def test_latest_instance_field(
    default_organization: models.Organization, instance
):
    """Test latest_instance field is updated when a new instance is created."""
    assert instance.latest_instance is None

    kwargs = {
        "name": "test-instance",
        "status": ActivationStatus.PENDING,
        "organization": default_organization,
    }

    if isinstance(instance, models.Activation):
        kwargs["activation"] = instance

    first_instance = models.RulebookProcess.objects.create(**kwargs)
    assert instance.latest_instance == first_instance

    second_instance = models.RulebookProcess.objects.create(**kwargs)
    assert instance.latest_instance == second_instance

    # ensure latest instance is returned when a previous instance is updated
    first_instance.status = ActivationStatus.COMPLETED
    first_instance.save(update_fields=["status"])
    assert instance.latest_instance == second_instance


@pytest.mark.parametrize(
    "instance",
    [
        pytest.param(
            lazy_fixture("new_activation"),
            id="activation",
        ),
    ],
)
@pytest.mark.django_db
def test_on_delete_process_parent_mixin(instance):
    """Test on_delete_process_parent_mixin."""
    queue_item = models.ActivationRequestQueue.objects.create(
        process_parent_type=instance.get_parent_type(),
        process_parent_id=instance.id,
        request=ActivationRequest.AUTO_START,
    )
    instance.delete()
    assert not models.ActivationRequestQueue.objects.filter(
        id=queue_item.id
    ).exists()

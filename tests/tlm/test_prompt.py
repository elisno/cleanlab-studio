import asyncio
from typing import Any

import pytest

from cleanlab_studio.studio.trustworthy_language_model import TLM


def is_tlm_response(response: Any) -> bool:
    """Returns True if the response is a TLMResponse."""
    return (
        isinstance(response, dict)
        and "response" in response
        and "trustworthiness_score" in response
    )


def test_single_prompt(tlm: TLM) -> None:
    """Tests running a single prompt in the TLM.

    Expected:
    - TLM should return a single response
    - Response should be non-None
    - No exceptions are raised
    """
    # act -- run a single prompt
    response = tlm.prompt("What is the capital of France?")

    # assert
    # - response is not None
    # - a single response of type TLMResponse is returned
    # - no exceptions are raised (implicit)
    assert response is not None
    assert is_tlm_response(response)


def test_batch_prompt(tlm: TLM) -> None:
    """Tests running a batch prompt in the TLM.

    Expected:
    - TLM should return a list of responses
    - Responses should be non-None
    - No exceptions are raised
    - Each response should be of type TLMResponse
    """
    # act -- run a batch prompt
    response = tlm.prompt(["What is the capital of France?"] * 3)

    # assert
    # - response is not None
    # - a list of responses of type TLMResponse is returned
    # - no exceptions are raised (implicit)
    assert response is not None
    assert isinstance(response, list)
    assert all(is_tlm_response(r) for r in response)


def test_batch_prompt_force_timeouts(tlm: TLM) -> None:
    """Tests running a batch prompt in the TLM, forcing timeouts.

    Sets timeout to 0.0001 seconds, which should force a timeout for all prompts.
    This should result in a timeout error being thrown

    Expected:
    - TLM should raise a timeout error
    """
    # arrange -- override timeout
    tlm._timeout = 0.0001

    # assert -- timeout is thrown
    with pytest.raises(asyncio.TimeoutError):
        # act -- run a batch prompt
        tlm.prompt(["What is the capital of France?"] * 3)


def test_batch_try_prompt(tlm: TLM) -> None:
    """Tests running a batch try prompt in the TLM.

    Expected:
    - TLM should return a list of responses
    - Responses can be None or of type TLMResponse
    - No exceptions are raised
    """
    # act -- run a batch prompt
    response = tlm.try_prompt(["What is the capital of France?"] * 3)

    # assert
    # - response is not None
    # - a list of responses of type TLMResponse or None is returned
    # - no exceptions are raised (implicit)
    assert response is not None
    assert isinstance(response, list)
    assert all(r is None or is_tlm_response(r) for r in response)


def test_batch_try_prompt_force_timeouts(tlm: TLM) -> None:
    """Tests running a batch try prompt in the TLM, forcing timeouts.

    Sets timeout to 0.0001 seconds, which should force a timeout for all prompts.
    This should result in None responses for all prompts.

    Expected:
    - TLM should return a list of responses
    - Responses can be None or of type TLMResponse
    - No exceptions are raised
    """
    # arrange -- override timeout
    tlm._timeout = 0.0001

    # act -- run a batch prompt
    response = tlm.try_prompt(["What is the capital of France?"] * 3)

    # assert
    # - response is not None
    # - all responses timed out and are None
    # - no exceptions are raised (implicit)
    assert response is not None
    assert isinstance(response, list)
    assert all(r is None for r in response)

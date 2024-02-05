import pytest
from unittest import mock
from datetime import datetime, timedelta, timezone
import asyncio
from aiohttp import ClientSession
from switchgrid_python_client import SwitchgridData, SwitchgridEventsResponse, Event
from asynctest import CoroutineMock, patch


@patch("aiohttp.ClientSession.get")
@pytest.mark.asyncio
async def test_update_with_successful_response(mock_get):
    mock_get.return_value.__aenter__.return_value.status = 200
    mocked_response = {
        "events": [
            {
                "eventId": "908fa861-c6e8-42b3-ab80-182427940ab3",
                "startUtc": "2024-02-05T23:00:00.000+01:00",
                "endUtc": "2024-02-06T00:00:00.000+01:00",
                "summary": "Effacement",
                "description": "⚡️ La consommation sera réduite pendant 1 heure.",
            }
        ]
    }
    mock_get.return_value.__aenter__.return_value.json = CoroutineMock(
        side_effect=[mocked_response]
    )

    session = ClientSession()
    sd = SwitchgridData(session)

    await sd.update()

    print(sd._last_response)

    jls_extract_var = SwitchgridEventsResponse(
        events=[
            Event(
                summary="Effacement",
                description="⚡️ La consommation sera réduite pendant 1 heure.",
                startUtc=datetime(
                    2024,
                    2,
                    5,
                    23,
                    0,
                    tzinfo=timezone(timedelta(seconds=3600)),
                ),
                endUtc=datetime(
                    2024,
                    2,
                    6,
                    0,
                    0,
                    tzinfo=timezone(timedelta(seconds=3600)),
                ),
                eventId="908fa861-c6e8-42b3-ab80-182427940ab3",
            )
        ]
    )
    print(jls_extract_var)
    assert sd._last_response == jls_extract_var
    assert sd._last_updated == datetime.now().strftime("%Y-%m-%d %H:%M:%S")

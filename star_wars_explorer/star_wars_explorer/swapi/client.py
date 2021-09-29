from typing import Generator

import requests
from memoize import memoize


@memoize(timeout=60 * 60 * 24)
def fetch_data(url: str) -> dict:
    """Utility for cached data fetching."""
    response = requests.get(url)
    # TODO response error handling
    return response.json()


class SWAPIClient:
    """TODO"""

    BASE_URL = "https://swapi.dev/api"

    def _probe_people(self, people: list, fetch_deep_fields: list) -> list:
        """Fetch additional associated data."""
        if not fetch_deep_fields:
            return people

        people = people[:]
        for person in people:
            for deep_field in fetch_deep_fields:
                deep_field_url = person[deep_field]
                person[deep_field] = fetch_data(deep_field_url)

        return people

    def get_people(self, fetch_deep_fields: list = ["homeworld"]) -> Generator:
        """Fetch all characters from Star Wars."""

        # TODO asyncio solution would be much better

        url = f"{self.BASE_URL}/people"
        data = fetch_data(url)

        yield from self._probe_people(
            people=data["results"], fetch_deep_fields=fetch_deep_fields
        )

        next_url = data.get("next")
        while next_url:
            data = fetch_data(next_url)
            next_url = data.get("next")
            yield from self._probe_people(
                people=data["results"], fetch_deep_fields=fetch_deep_fields
            )

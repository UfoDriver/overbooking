class TestReservations:
    URL = '/api/v1/reservations'

    async def test_get_reservations(self, client):
        resp = await client.get(self.URL)
        assert resp.status == 200
        payload = await resp.json()
        assert payload == {'suits': 100,
                           'booked': 99,
                           'max': 110}

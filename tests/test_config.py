class TestConfig:
    URL = '/api/v1/config'

    async def test_get_config(self, client):
        resp = await client.get(self.URL)
        assert resp.status == 200
        payload = await resp.json()
        assert payload == {'suits': 100,
                           'overbooking': 10}

    async def test_post_config(self, client):
        data = {'suits': 200, 'overbooking': 5}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 201
        payload = await resp.json()
        assert payload == {'suits': 200, 'overbooking': 5}

        resp = await client.get(self.URL)
        assert resp.status == 200
        payload = await resp.json()
        assert payload == {'suits': 200,
                           'overbooking': 5}

    async def test_post_invalid_suites(self, client):
        data = {'suits': 'broken', 'overbooking': 5}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 400
        payload = await resp.json()
        assert payload == {'suits': '"broken" is not a number'}

    async def test_post_invalid_overbooking(self, client):
        data = {'suits': '100', 'overbooking': 'broken'}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 400
        payload = await resp.json()
        assert payload == {'overbooking': '"broken" is not a number'}

    async def test_post_negative_suites(self, client):
        data = {'suits': -1, 'overbooking': 5}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 400
        payload = await resp.json()
        assert payload == {'suits': 'Should be greater than 0'}

    async def test_post_negative_overbooking(self, client):
        data = {'suits': '100', 'overbooking': -1}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 400
        payload = await resp.json()
        assert payload == {'overbooking': '-1 is less than minimum value 0'}

    async def test_post_allowed_lowering(self, client):
        data = {'suits': '100', 'overbooking': 1}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 201
        payload = await resp.json()
        assert payload == {'overbooking': 1, 'suits': 100}

    async def test_post_edge_allowed_lowering(self, client):
        data = {'suits': '90', 'overbooking': 10}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 201
        payload = await resp.json()
        assert payload == {'overbooking': 10, 'suits': 90}

    async def test_post_not_allowed_lowering(self, client):
        data = {'suits': '90', 'overbooking': 5}
        resp = await client.post(self.URL, data=data)
        assert resp.status == 412
        payload = await resp.json()
        assert payload == {'error': 'Cannot lower suits number or prebooking value'}

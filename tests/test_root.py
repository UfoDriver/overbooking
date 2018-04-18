async def test_root(client):
    resp = await client.get('/')
    assert resp.status == 404
    text = await resp.text()
    assert text == '404: Not Found'

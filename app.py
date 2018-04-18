from aiohttp import web

from schemas import ConfigSchema


routes = web.RouteTableDef()


def max_suits(suits, overbooking):
    return suits + int(suits * overbooking / 100)


async def startup(app):
    print('Startup')


async def shutdown(app):
    print('Shutdown')


@routes.view('/api/v1/reservations')
class ReservationsView(web.View):
    async def get(self):
        data = self.request.app['data']
        return web.json_response({'suits': data['SUITS_COUNT'],
                                  'booked': data['BOOKED'],
                                  'max': max_suits(data['SUITS_COUNT'],
                                                   data['OVERBOOKING'])})


@routes.view('/api/v1/config')
class ConfigView(web.View):
    async def get(self):
        return web.json_response({
            'suits': self.request.app['data']['SUITS_COUNT'],
            'overbooking': self.request.app['data']['OVERBOOKING']})

    async def post(self):
        data = await self.request.post()

        try:
            data = ConfigSchema().deserialize(data)
        except ConfigSchema.Invalid as e:
            return web.json_response(e.asdict(), status=400)

        new_suits, new_overbooking = data['suits'], data['overbooking']

        # Check if we can set new suits cound and overbooking
        if self.request.app['data']['BOOKED'] > max_suits(new_suits, new_overbooking):
            return web.json_response(
                {'error': 'Cannot lower suits number or prebooking value'},
                status=412)

        self.request.app['data']['SUITS_COUNT'] = new_suits
        self.request.app['data']['OVERBOOKING'] = new_overbooking

        return web.json_response({'suits': self.request.app['data']['SUITS_COUNT'],
                                  'overbooking': self.request.app['data']['OVERBOOKING']},
                                 status=201)


def create_app(loop):
    app = web.Application(loop=loop)
    app.add_routes(routes)

    app['data'] = {
        'SUITS_COUNT': 100,
        'BOOKED': 99,
        'OVERBOOKING': 10
    }

    return app

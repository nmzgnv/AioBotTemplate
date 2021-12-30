import asyncio
import multiprocessing
import os

from gino_admin import add_admin_panel
from sanic import Sanic, response
from loguru import logger
from bot.main import init_bot
from config import DB_NAME, DB_USER, DB_PASSWORD, DATABASE_URL, DB_HOST
from daemon.main import init_daemon
from models import User, Text, db
from sanic_jinja2 import SanicJinja2

app = Sanic(name=__name__)
jinja = SanicJinja2(app, pkg_name="server")
logger.add("data.log", format='{time} {level} {message}', level="INFO", rotation="10 MB", compression="zip")

telegram_bot = multiprocessing.Process(target=init_bot)


@app.route("/")
async def index(request):
    return response.redirect("/admin")


async def redirect_to_bot_settings(request):
    return response.redirect("/bot-settings")


@app.route("/bot-settings")
def bot_settings(request):
    token = os.getenv('BOT_TOKEN')
    return jinja.render("bot_settings.html", request, token=token)


def generate_response_message(is_success, message):
    return {'success': is_success, 'message': message}


@app.route("/api/bot/stop")
def stop_bot_handle(request):
    if telegram_bot.is_alive():
        stop_bot_process()
        response_data = generate_response_message(True, 'Bot was turned off')
    else:
        response_data = generate_response_message(False, 'Bot already turned off')

    return response.json(response_data)


@app.route("/api/bot/restart")
def start_bot_handle(request):
    restart_bot_process()
    return response.json(generate_response_message(True, 'Bot was restarted'))


@app.route("/api/bot/change-token", methods=['POST', 'PUT'])
def start_bot_handle(request):
    data = request.json

    if 'token' in data:
        new_token = data['token']
        os.environ['BOT_TOKEN'] = new_token
        restart_bot_process()
        response_data = generate_response_message(True, 'Bot token was updated. Bot restarted.')
    else:
        response_data = generate_response_message(False, 'Invalid request body')

    return response.json(response_data)


def stop_bot_process():
    global telegram_bot
    telegram_bot.terminate()
    telegram_bot.kill()
    logger.info("Bot was turned off")


def start_new_bot_process():
    global telegram_bot
    telegram_bot = multiprocessing.Process(target=init_bot)
    telegram_bot.start()
    logger.info("Bot process was started")


def restart_bot_process():
    stop_bot_process()
    start_new_bot_process()


async def init_db():
    await db.set_bind(DATABASE_URL)
    # await db.gino.drop_all()
    await db.gino.create_all()
    await db.pop_bind().close()


def init_server() -> Sanic:
    app.config["DB_HOST"] = DB_HOST
    app.config["DB_DATABASE"] = DB_NAME
    app.config["DB_USER"] = DB_USER
    app.config["DB_PASSWORD"] = DB_PASSWORD

    # app.config["ADMIN_USER"] = "admin"
    # app.config["ADMIN_PASSWORD"] = "admin"
    os.environ['ADMIN_AUTH_DISABLE'] = '1'

    add_admin_panel(
        name='Bot admin',
        app=app,
        db=db,
        db_models=[User, Text],
        hide_columns=['pk', 'id']
    )
    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    # TODO asyncio run checkpoints
    # 1) Token exist
    # 2) Tables exist

    daemon = multiprocessing.Process(target=init_daemon)
    daemon.start()
    telegram_bot.start()

    app = init_server()
    # Override gino admin link to be able to redirect to my custom page
    for route in app.router.routes:
        if route.path == 'admin/settings':
            route.handler = redirect_to_bot_settings
            break

    logger.info("App has been initialized")
    app.run(host="127.0.0.1", port=os.getenv("PORT", 8000), debug=False, auto_reload=False)

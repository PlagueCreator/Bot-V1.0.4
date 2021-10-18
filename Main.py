import fortnitepy
import json
import os

from fortnitepy.ext import commands

email = 'botemail@gmail.com'
password = 'password1'
filename = 'device_auths.json'

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)

device_auth_details = get_device_auth_details().get(email, {})
bot = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=email,
        password=password,
        prompt_authorization_code=True,
        prompt_code_if_invalid=True,
        delete_existing_device_auths=True,
        **device_auth_details
    )
)

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@bot.event
async def event_ready():
    print('----------------')
    print('il tuo bot è pronto')
    print(bot.user.display_name)
    print(bot.user.id)
    print('----------------')

@bot.event
async def event_friend_request(request):
    await request.accept()

@bot.command()
async def hello(ctx):
    await ctx.send('sei un coglione')

bot.run()



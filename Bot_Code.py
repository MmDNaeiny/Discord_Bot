import discord
from discord.ext import commands
from discord import SelectOption, ui
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents) # میتونه از اینجا پرفیکس بات رو تنظیم کنید که از طریق / اسلش باشه یا خیر 
ticket_counter = 1001  # شمارنده تیکت‌ها

@bot.event
async def on_ready():
    print('Bot Run Shod.')
    # while True:
    #     await bot.change_presence(status=discord.Status.do_not_disturb)
    #     await asyncio.sleep(1) 
    #     await bot.change_presence(status=discord.Status.online)
    #     await asyncio.sleep(1) 
    #     await bot.change_presence(status=discord.Status.idle)
    #     await asyncio.sleep(1)  
    # await bot.change_presence(activity=discord.Game(name="اسم چیزی که میخواید مثلا بنویسه در حال پلی دادن فلان ..."))

@bot.event
async def on_guild_channel_create(channel):
    YOUR_TICKET_CATEGORY_ID = 123456789123456789  # آیدی کتگوری که تیکت ها توش باز میشه
    if channel.category_id == YOUR_TICKET_CATEGORY_ID:
        await create_dropdown(channel)

class TicketDropdown(ui.Select):
    def __init__(self):
        options=[
            SelectOption(label='درخواست آنبن', value='درخواست آنبن'), #اسم زیر منو ها
            SelectOption(label='خانه', value='خانه'), #اسم زیر منو ها
            SelectOption(label='دونیت', value='دونیت') #اسم زیر منو ها
        ]
        super().__init__(placeholder='یک گزینه را انتخاب کنید', min_values=1, max_values=1, options=options) #متنی که بصورت کمرنگ تر در زیر منو نوشته شده و وقتی میزنه باز شه پنهان میشه

    async def callback(self, interaction: discord.Interaction):
        global ticket_counter  # استفاده از شمارنده جهانی
        selected_option = self.values[0]
        new_name = f"{selected_option}-{ticket_counter}"
        ticket_counter += 1  # افزایش شمارنده
        await interaction.channel.edit(name=new_name)
        await interaction.response.send_message(f'کانال به {new_name} تغییر نام یافت.', ephemeral=True)
        await interaction.message.delete()  # حذف پیام بعد از انتخاب موضوع دراپ داون

class TicketDropdownView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketDropdown())

async def create_dropdown(channel):
    await asyncio.sleep(1)  # تأخیر 1 ثانیه‌ای در زمان فرستادن پیام بعد از باز شدن تیکت که بعد از پیام تیکت تول بیاد
    view = TicketDropdownView()
    await channel.send('لطفا یک گزینه را انتخاب کنید:', view=view) #متنی که بالای دراپ داون استایل می نویسه

bot.run('Bot Token') #توکن باتی که نوشتید
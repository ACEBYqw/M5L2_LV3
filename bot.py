from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Kullanıcı işaretçi rengi ve nokta listesi
bot.marker_color = "red"
bot.points = []

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

# -----------------------------
# Başlat ve yardım komutları
# -----------------------------
@bot.command()
async def start(ctx):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutların listesini keşfetmek için !help_me yazın.")

@bot.command()
async def help_me(ctx):
    help_text = (
        "**Mevcut Komutlar:**\n"
        "`!start` - Botu başlatır ve hoş geldin mesajı gönderir.\n"
        "`!remember_city <şehir>` - Şehri veritabanına kaydeder.\n"
        "`!show_city <şehir>` - Belirtilen şehri harita üzerinde gösterir.\n"
        "`!show_my_cities` - Kaydettiğiniz tüm şehirleri harita üzerinde gösterir.\n"
        "`!distance <şehir1> <şehir2>` - İki şehir arasına mavi çizgi çizer ve haritayı gösterir.\n"
        "`!renk <color>` - İşaretçilerin rengini seçer.\n"
        "`!nokta <lat> <lon>` - Haritaya nokta ekler ve gösterir.\n"
        "`!temizle` - Haritadaki tüm noktaları temizler."
    )
    await ctx.send(help_text)

# -----------------------------
# İşaretçi rengi seçimi
# -----------------------------
@bot.command()
async def renk(ctx, color: str):
    """Kullanıcı işaretçi rengini seçer."""
    bot.marker_color = color
    await ctx.send(f"İşaretçi rengi {color} olarak ayarlandı!")

# -----------------------------
# Nokta ekleme ve harita gösterme
# -----------------------------
@bot.command()
async def nokta(ctx, lat: float, lon: float):
    """Kullanıcı haritaya nokta ekler ve gösterir."""
    bot.points.append((lat, lon))
    image_buf = harita_olustur(bot.points, marker_color=bot.marker_color)
    await ctx.send(file=discord.File(fp=image_buf, filename="harita.png"))

@bot.command()
async def temizle(ctx):
    """Haritadaki tüm noktaları temizler."""
    bot.points.clear()
    await ctx.send("Tüm noktalar temizlendi!")

# -----------------------------
# Mevcut şehir komutları
# -----------------------------
@bot.command()
async def show_city(ctx, *, city_name=""):
    if not city_name:
        await ctx.send("Lütfen bir şehir adı girin. Örnek: `!show_city Paris`")
        return

    coords = manager.get_coordinates(city_name)
    if not coords:
        await ctx.send("Bu şehir veri tabanında bulunamadı.")
        return

    image_path = f"{city_name}_map.png"
    manager.create_graph(image_path, [city_name])
    await ctx.send(file=discord.File(image_path))

@bot.command()
async def show_my_cities(ctx):
    cities = manager.select_cities(ctx.author.id)
    if not cities:
        await ctx.send("Henüz hiçbir şehir kaydetmediniz. Eklemek için `!remember_city <şehir>` yazın.")
        return

    image_path = f"{ctx.author.id}_cities_map.png"
    manager.create_graph(image_path, cities)
    await ctx.send(file=discord.File(image_path))

@bot.command()
async def remember_city(ctx, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):
        await ctx.send(f'{city_name} şehri başarıyla kaydedildi!')
    else:
        await ctx.send("Hatalı format. Lütfen şehir adını İngilizce olarak ve komuttan sonra bir boşluk bırakarak girin.")

@bot.command()
async def distance(ctx, *, cities=""):
    parts = cities.split()
    if len(parts) != 2:
        await ctx.send("Lütfen iki şehir adı girin. Örnek: `!distance Paris London`")
        return

    city1, city2 = parts
    manager.draw_distance(city1, city2)
    await ctx.send(file=discord.File("distance_map.png"))

# -----------------------------
# Bot çalıştır
# -----------------------------
if __name__ == "__main__":
    bot.run(TOKEN)

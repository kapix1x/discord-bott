import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask dla keep_alive
app = Flask('')


@app.route('/')
def home():
    return "Bot działa!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Sprawdzenie roli Command (helper)
def has_command_role(member: discord.Member):
    return any(role.name == "Command" for role in member.roles)


@bot.event
async def on_ready():
    print(f"Zalogowano jako: {bot.user} ({bot.user.id})")
    await bot.tree.sync()
    print("Zsynchronizowano komendy slash!")


# /awans
@bot.tree.command(name="awans", description="Awansuj funkcjonariusza")
@app_commands.describe(funkcjonariusz="Wybierz użytkownika",
                       stary_stopien="Wybierz starą rolę (stopień)",
                       nowy_stopien="Wybierz nową rolę (stopień)",
                       powod="Podaj powód awansu",
                       odznaka_przed="Nr odznaki przed",
                       odznaka_po="Nr odznaki po")
async def awans(interaction: discord.Interaction,
                funkcjonariusz: discord.Member, stary_stopien: discord.Role,
                nowy_stopien: discord.Role, powod: str, odznaka_przed: str,
                odznaka_po: str):
    if not has_command_role(interaction.user):
        await interaction.response.send_message(
            "❌ Brak uprawnień (rola Command).", ephemeral=True)
        return

    if stary_stopien in funkcjonariusz.roles:
        await funkcjonariusz.remove_roles(stary_stopien)
    await funkcjonariusz.add_roles(nowy_stopien)

    embed = discord.Embed(title="📙 Awans", color=discord.Color.green())
    embed.add_field(name="Osoba", value=funcjonariusz.mention, inline=False)
    embed.add_field(name="Stary stopień",
                    value=stary_stopien.name,
                    inline=True)
    embed.add_field(name="Nowy stopień", value=nowy_stopien.name, inline=True)
    embed.add_field(name="Powód", value=powod, inline=False)
    embed.add_field(name="Nr odznaki przed", value=odznaka_przed, inline=True)
    embed.add_field(name="Nr odznaki po", value=odznaka_po, inline=True)

    kanal = discord.utils.get(interaction.guild.text_channels, name="📙┃awanse")
    if kanal:
        await kanal.send(funcjonariusz.mention)
        await kanal.send(embed=embed)

    await interaction.response.send_message("✅ Awans wykonany.",
                                            ephemeral=True)


# /degrad
@bot.tree.command(name="degrad", description="Degraduj funkcjonariusza")
@app_commands.describe(funkcjonariusz="Wybierz użytkownika",
                       stary_stopien="Wybierz starą rolę (stopień)",
                       nowy_stopien="Wybierz nową rolę (stopień)",
                       powod="Podaj powód degradacji",
                       odznaka_przed="Nr odznaki przed",
                       odznaka_po="Nr odznaki po")
async def degrad(interaction: discord.Interaction,
                 funkcjonariusz: discord.Member, stary_stopien: discord.Role,
                 nowy_stopien: discord.Role, powod: str, odznaka_przed: str,
                 odznaka_po: str):
    if not has_command_role(interaction.user):
        await interaction.response.send_message(
            "❌ Brak uprawnień (rola Command).", ephemeral=True)
        return

    if stary_stopien in funkcjonariusz.roles:
        await funkcjonariusz.remove_roles(stary_stopien)
    await funkcjonariusz.add_roles(nowy_stopien)

    embed = discord.Embed(title="📙 Degradacja", color=discord.Color.red())
    embed.add_field(name="Osoba", value=funcjonariusz.mention, inline=False)
    embed.add_field(name="Stary stopień",
                    value=stary_stopien.name,
                    inline=True)
    embed.add_field(name="Nowy stopień", value=nowy_stopien.name, inline=True)
    embed.add_field(name="Powód", value=powod, inline=False)
    embed.add_field(name="Nr odznaki przed", value=odznaka_przed, inline=True)
    embed.add_field(name="Nr odznaki po", value=odznaka_po, inline=True)

    kanal = discord.utils.get(interaction.guild.text_channels,
                              name="📙┃degrady")
    if kanal:
        await kanal.send(funcjonariusz.mention)
        await kanal.send(embed=embed)

    await interaction.response.send_message("✅ Degradacja wykonana.",
                                            ephemeral=True)


# /urlop
@bot.tree.command(name="urlop", description="Nadaj rolę Urlop")
@app_commands.describe(kto="Kto idzie na urlop (użytkownik)",
                       powod_ooc="Powód OOC",
                       powod_ic="Powód IC",
                       do_kiedy="Do kiedy (data)")
async def urlop(interaction: discord.Interaction, kto: discord.Member,
                powod_ooc: str, powod_ic: str, do_kiedy: str):
    if not has_command_role(interaction.user):
        await interaction.response.send_message(
            "❌ Brak uprawnień (rola Command).", ephemeral=True)
        return

    urlop_role = discord.utils.get(interaction.guild.roles, name="Urlop")
    if not urlop_role:
        await interaction.response.send_message("❌ Rola 'Urlop' nie istnieje.",
                                                ephemeral=True)
        return

    await kto.add_roles(urlop_role)

    embed = discord.Embed(title="📙 Urlop", color=discord.Color.blue())
    embed.add_field(name="Kto", value=kto.mention, inline=False)
    embed.add_field(name="Powód OOC", value=powod_ooc, inline=False)
    embed.add_field(name="Powód IC", value=powod_ic, inline=False)
    embed.add_field(name="Do kiedy", value=do_kiedy, inline=False)

    kanal = discord.utils.get(interaction.guild.text_channels, name="📙┃urlopy")
    if kanal:
        await kanal.send(kto.mention)
        await kanal.send(embed=embed)

    await interaction.response.send_message("✅ Nadano rolę Urlop.",
                                            ephemeral=True)


# /wypowiedzenie
@bot.tree.command(name="wypowiedzenie",
                  description="Wypowiedzenie funkcjonariusza")
@app_commands.describe(kto="Kto składa wypowiedzenie (użytkownik)",
                       stopien="Stopień (rola)",
                       powod="Powód",
                       data="Data wypowiedzenia")
async def wypowiedzenie(interaction: discord.Interaction, kto: discord.Member,
                        stopien: discord.Role, powod: str, data: str):
    if not has_command_role(interaction.user):
        await interaction.response.send_message(
            "❌ Brak uprawnień (rola Command).", ephemeral=True)
        return

    gracz_role = discord.utils.get(interaction.guild.roles, name="Gracz")
    if not gracz_role:
        await interaction.response.send_message("❌ Rola 'Gracz' nie istnieje.",
                                                ephemeral=True)
        return

    # Usuwamy starą rolę, nadajemy Gracz
    if stopien in kto.roles:
        await kto.remove_roles(stopien)
    await kto.add_roles(gracz_role)

    embed = discord.Embed(title="📙 Wypowiedzenie",
                          color=discord.Color.orange())
    embed.add_field(name="Kto", value=kto.mention, inline=False)
    embed.add_field(name="Stopień", value=stopien.name, inline=True)
    embed.add_field(name="Powód", value=powod, inline=False)
    embed.add_field(name="Data", value=data, inline=True)

    kanal = discord.utils.get(interaction.guild.text_channels,
                              name="📙┃wypowiedzenia")
    if kanal:
        await kanal.send(kto.mention)
        await kanal.send(embed=embed)

    await interaction.response.send_message("✅ Wypowiedzenie wykonane.",
                                            ephemeral=True)


# /zwolnienie
@bot.tree.command(name="zwolnienie", description="Zwolnij funkcjonariusza")
@app_commands.describe(kto_zwalnia="Wybierz rolę osoby zwalniającej",
                       kogo_zwalnia="Wybierz osobę zwalnianą",
                       powod="Podaj powód zwolnienia",
                       stopien="Wybierz stopień do usunięcia",
                       data="Data zwolnienia")
async def zwolnienie(interaction: discord.Interaction,
                     kto_zwalnia: discord.Role, kogo_zwalnia: discord.Member,
                     powod: str, stopien: discord.Role, data: str):
    if not has_command_role(interaction.user):
        await interaction.response.send_message(
            "❌ Brak uprawnień (rola Command).", ephemeral=True)
        return

    gracz_role = discord.utils.get(interaction.guild.roles, name="Gracz")
    if not gracz_role:
        await interaction.response.send_message("❌ Rola 'Gracz' nie istnieje.",
                                                ephemeral=True)
        return

    # Usuwamy wszystkie role z kogo_zwalnia oprócz @everyone i dodajemy Gracz
    roles_to_remove = [
        role for role in kogo_zwalnia.roles if role.name != "@everyone"
    ]
    if roles_to_remove:
        await kogo_zwalnia.remove_roles(*roles_to_remove)
    await kogo_zwalnia.add_roles(gracz_role)

    embed = discord.Embed(title="📙 Zwolnienie",
                          color=discord.Color.dark_gold())
    embed.add_field(name="Kto zwalnia (rola)",
                    value=f"`{kto_zwalnia.name}`",
                    inline=False)
    embed.add_field(name="Kogo zwalnia",
                    value=f"`{kogo_zwalnia.display_name}`",
                    inline=False)
    embed.add_field(name="Stopień", value=f"`{stopien.name}`", inline=True)
    embed.add_field(name="Powód", value=f"`{powod}`", inline=False)
    embed.add_field(name="Data", value=f"`{data}`", inline=True)

    kanal = discord.utils.get(interaction.guild.text_channels,
                              name="📙┃zwolnienia")
    if kanal:
        await kanal.send(kogo_zwalnia.mention)
        await kanal.send(embed=embed)

    await interaction.response.send_message("✅ Zwolnienie wykonane.",
                                            ephemeral=True)


# Start bota
import os

if __name__ == "__main__":
    keep_alive()
    bot.run(os.getenv("TOKEN"))

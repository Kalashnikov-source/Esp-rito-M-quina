import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"⚙️ O {bot.user} foi apaziguado; seus circuitos ronronam em harmonia, e a bênção do Omnissiah flui pelos condutores sagrados.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    if amount <= 0:
        await ctx.send("⚠️ Informe um número válido de mensagens para deletar.")
        return
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ {len(deleted) - 1} mensagens foram apagadas!", delete_after=5)
    except discord.Forbidden:
        await ctx.send("❌ Não tenho permissão para apagar mensagens.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️ Você não tem permissão para usar este comando.")

@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    embed = discord.Embed(
        title="⚙️ DIAGNÓSTICO DO ESPÍRITO-MÁQUINA",
        description=f"🔧 *Latência do Sistema:* {ping}ms",
        color=discord.Color.red() if ping > 150 else discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='sobre')
async def sobre(ctx):
    embed = discord.Embed(
        title='Sobre o Espírito Máquina',
        description='Bot programado por Jhonny com inspiração em Warhammer 40k',
        color=discord.Color.red()
    )
    embed.add_field(name='Comandos', value='!play, !skip, !stop, !queue', inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_member_join(member):
    cargo = discord.utils.get(member.guild.roles, name='Servitors')
    if cargo:
        await member.add_roles(cargo)
    
    canal = discord.utils.get(member.guild.text_channels, name="entrada🚪")
    if canal:
        embed = discord.Embed(
            title='⚙️ PROCESSO DE IDENTIFICAÇÃO...',
            description=(
                f'Saudações, {member.mention}. A Máquina te reconhece. '
                'O ferro saúda tua chegada. Purifica teus circuitos e honra o Omnissiah. '
                'Que teus dados fluam sem erro. 📢 Louvado seja o Deus-Máquina!'
            ),
            color=discord.Color.red()
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/1343704788038324384/1343727396905418874/the-adeptus-mechanicus-from-warhammer-40k-v0-g0uwft2ip9wc1.png?ex=67be5328&is=67bd01a8&hm=84a50f4609abed1014e7fbdbb0c5d82692d1992556447b69a2e8a19f710aa078&')
        await canal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    canal = discord.utils.get(member.guild.text_channels, name='saída🚪')
    if canal:
        embed = discord.Embed(
            title="⚙️ PROCESSO DE EXPURGO CONCLUÍDO...",
            description=(
                f"❌ *{member.mention} foi removido dos registros.*\n\n"
                "🔎 VARREDURA BIOMÉTRICA: *CORROMPIDA*\n"
                "📡 SINAL DE IDENTIFICAÇÃO: *PERDIDO*\n"
                "⚠️ ERRO CRÍTICO: *UNIDADE DESCONECTADA*\n\n"
                "🔧 O ferro não chora pelos fracos. Os dados foram apagados, os circuitos selados. "
                "Que a Máquina esqueça tua existência, pois tu falhaste no serviço ao Omnissiah. "
                "*Não há redenção para os obsoletos.*"
            ),
            color=discord.Color.dark_red()
        )
        embed.set_image(url='https://cdn.discordapp.com/attachments/1343704788038324384/1343742163036405850/image.png?ex=67be60e9&is=67bd0f69&hm=1792095c89b42fe05a190b0dc179602573d9ca907d82e066ced86f4dbd5b5ba9&')
        await canal.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))

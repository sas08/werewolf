import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from typing import Optional


class SlashWolf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.slash.get_cog_commands(self)  # コマンドを取得する
        # asyncio.create_task(self.bot.slash.sync_all_commands()) # 同期してコマンドがDiscordに出るようにする

    # コマンドの定義はcog_ext.cog_slashデコレータを使う
    @cog_ext.cog_slash(
        name='fortun',
        description='占い対象の指定　　role[discord.Role]: ロールメンション',
        guild_ids=[720566804094648330, 808283612105408533, 726233332655849514]
    )
    async def slash_say(self, ctx: SlashContext, role: Optional[discord.Role]):
        if not self.bot.system.fortun.can_move:
            await ctx.send("実行に失敗しました。")
            return

        try:
            member = role.members[0]
        except IndexError:
            txt = "誰も占いませんでした。"
        else:
            user_id = ctx.author_id
            player = None
            yes = 0
            for p in self.bot.system.player.live:
                if user_id == p.id:
                    player = p
                if member.id == p.id:
                    yes += 1
            if player:
                if player.role != "占い師":
                    await ctx.send("あなたは占い師ではありません。")
                    return
            if yes == 0:
                txt = "誰も占いませんでした"
            elif role.name == "人狼参加者":
                txt = "誰も占いませんでした"
            elif role.name == "死亡者":
                txt = "誰も占いませんでした"
            elif role.name == "観戦者":
                txt = "誰も占いませんでした"
            else:
                txt = f"{member.mention} を占います"
                self.bot.system.fortun.flag = member
                self.bot.system.fortun.can_move = False

        await ctx.send(content=txt, hidden=False)  # hidden=Trueで実行した人のみにみえるように

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)  # コマンド解放


def setup(bot):
    bot.add_cog(SlashWolf(bot))

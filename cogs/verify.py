import disnake
from disnake.ext import commands

class ReasonModal(disnake.ui.Modal):
    def __init__(self, name, age, info, user):
        self.name = name
        self.age = age
        self.info = info
        self.user = user
        components = [
            disnake.ui.TextInput(label="Причина отказа:", placeholder="Укажи причину", custom_id="reason")
        ]
        super().__init__(title="Отказ", components=components, custom_id="reasonmodal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = self.name
        age = self.age
        info = self.info
        reason = interaction.text_values["reason"]
        user = self.user
        embed = disnake.Embed(title='', color=disnake.Color.from_rgb(43,45,49))
        embed.add_field(name='', value=f'Заявку {user.mention} отклонил: {interaction.user.mention}', inline=False)
        embed.add_field(name='Имя:', value=f'```{name}```', inline=False)
        embed.add_field(name='Возраст 13>?:', value=f'```{age}```', inline=False)
        embed.add_field(name='Причина подачи:', value=f'```{info}```', inline=False)
        embed.add_field(name='Причина отказа:', value=f'```{reason}```', inline=False)
        embed.set_thumbnail(url=f'{interaction.user.avatar}')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&')
        await interaction.response.edit_message(embed=embed, view=None)

class Accept_Decline(disnake.ui.View):
    def __init__(self, name, age, info, user):
        self.name = name
        self.age = age
        self.info = info
        self.user = user
        super().__init__(timeout=None)
        
    @disnake.ui.button(label="Верифицировать", style=disnake.ButtonStyle.green, custom_id="accept_man")
    async def manbutton(self, button, interaction: disnake.MessageInteraction):
        name = self.name
        age = self.age
        info = self.info
        user = self.user
        verify = interaction.guild.get_role(1224042866784079936)
        pending_role = interaction.guild.get_role(1221873573506056224)
        await user.remove_roles(pending_role)
        await user.add_roles(verify)
        embed = disnake.Embed(title='', color=disnake.Color.from_rgb(43, 45, 49))
        embed.add_field(name='', value=f'{user.mention} был верифицирован {interaction.user.mention}', inline=False)
        embed.add_field(name='Имя:', value=f'```{name}```', inline=False)
        embed.add_field(name='Возраст 13>?:', value=f'```{age}```', inline=False)
        embed.add_field(name='Причина подачи:', value=f'```{info}```', inline=False)
        embed.set_thumbnail(url=f'{interaction.user.avatar}')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&')
        await interaction.response.edit_message(embed=embed, view=None)

    @disnake.ui.button(label="Отклонить", style=disnake.ButtonStyle.danger, custom_id="decline")
    async def declinebutton(self, button, interaction: disnake.MessageInteraction):
        name = self.name
        age = self.age
        info = self.info
        user = self.user
        await interaction.response.send_modal(ReasonModal(name, age, info, user))


class VerifyModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label="Как вас зовут?", placeholder="Ваше имя", custom_id="name", min_length=2, max_length=20),
            disnake.ui.TextInput(label="Вам больше 13?", placeholder="Да / Нет", custom_id="age", min_length=1, max_length=3),
            disnake.ui.TextInput(label="Почему хочешь получить доступ к серверу?", placeholder="Хочу новые знакомства", custom_id="info", min_length=5, max_length=80)
        ]
        super().__init__(title="Верификация", components=components, custom_id="verifymodal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        name = interaction.text_values["name"]
        age = interaction.text_values["age"]
        info = interaction.text_values["info"]
        user = interaction.author
        channel=interaction.guild.get_channel(1224047599770927298)
        support_role = interaction.guild.get_role(1221858474850390127)
        embed=disnake.Embed(title=f'Верифицируем?', color=disnake.Color.from_rgb(43,45,49))
        embed.add_field(name='Пинг:', value=f'{interaction.author.mention}', inline=False)
        embed.add_field(name='Имя:', value=f'```{name}```', inline=False)
        embed.add_field(name='Возраст:', value=f'```{age}```', inline=False)
        embed.add_field(name='Причина подачи:', value=f'```{info}```', inline=False)
        embed.set_thumbnail(url=f'{interaction.user.avatar}')
        embed.set_image(url='https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&')
        view = Accept_Decline(name, age, info, user)
        await channel.send(f"{support_role.mention}", embed=embed, view=view)
        await interaction.response.send_message("Твоя заявка на верификацию отправлена!", ephemeral=True)



class VerifyButton(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Верифицироваться", style=disnake.ButtonStyle.grey, custom_id="verify")
    async def button(self, button, interaction: disnake.MessageInteraction):
        await interaction.response.send_modal(VerifyModal())




class VerifyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    async def verify(self, ctx):
        embed = disnake.Embed(title="Верификация")
        embed.description = f'**Привет! Хочешь стать частью сервера Anorex CLXN? Для этого тебе нужно:**\n\n' \
                            f'* Написать заявку по форме ниже.\n\n' \
                            f'* Аккаунту должно быть больше 7 дней.\n\n' \
                            f'* Следовать правилам проекта.'
        embed.set_image(url="https://cdn.discordapp.com/attachments/1211275021713014854/1224093847890559099/image_10.png?ex=661c3d3b&is=6609c83b&hm=e0207f3964274b2a842c457a9d68f27c46db1f2b012d266d7e2bf9a547a1e250&")
        view = VerifyButton()
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        view = disnake.ui.View(timeout=None)
        view.add_item(disnake.ui.Button(label="Верифицироваться", style=disnake.ButtonStyle.grey, custom_id="verify"))
        self.bot.add_view(view, message_id=1224117153632878602)

def setup(bot):
    bot.add_cog(VerifyCogs(bot))
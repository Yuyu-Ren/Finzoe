# Base library requirements
import discord
from discord.ext import commands
import asyncio

# DB Functionality
import sqlite3

# Regex and pretty tabular output
import re
from tabulate import tabulate

# Set your DB path here
DB_PATH='./Finzoe.db'


class Birthday():
	def __init__(self, bot):
		self.bot = bot
		self.YMDRegex = r"^((1[0-2]|0?[1-9]))[\s./-](([1-2][0-9]|3[0-1]|0?[1-9]))$"

	# Get birthday list with empty command summon [PM]
	# Set birthday using <command> YYYY-mm-dd
	# Get other member birthday using <command> <@user_id>
	@commands.command()
	async def birthday(self, ctx, *, message:str=""):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		birthday_list = []
		if not message:
			birthday_list = c.execute('SELECT `Name`, `Date` FROM Birthdays').fetchall()
			if birthday_list:
				await ctx.send("```"+tabulate(birthday_list, headers=['Name', 'Date'])+"```")
			else:
				await ctx.send("There are no birthdays in the database to display :C")
		elif re.match(self.YMDRegex, message.strip()):
			temp = re.sub(r'[^\w]', '', ctx.message.author.name)
			t = (ctx.message.author.id, temp, message)
			# c.execute('REPLACE INTO Birthdays WHERE ID={}'.format(ctx.message.author.id))
			c.execute('REPLACE INTO Birthdays VALUES (?, ?, ?)', t)
			conn.commit()
			await ctx.send("{}'s birthday saved successfully!".format(temp))
			await asyncio.sleep(1)
		else:
			message = re.sub(r'[^\w ]', "", message)
			message_list = message.split()
			for item in message_list:
				birthday_list.extend(c.execute('SELECT `Name`, `Date` FROM Birthdays WHERE ID=? or Name LIKE ?', (item, "%"+item+"%")).fetchall())
			if birthday_list:
				await ctx.send("```"+tabulate(birthday_list, headers=['Name', 'Date'])+"```")
			else:
				await ctx.send("Sorry, I don't understand. Please check the command syntax and try again.")

def setup(bot):
	bot.add_cog(Birthday(bot))

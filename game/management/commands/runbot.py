from django.core.management.base import BaseCommand
import asyncio
from bot.main import main

class Command(BaseCommand):
    help = "Telegram botni ishga tushuradi (aiogram 3.x bilan)"

    def handle(self, *args, **options):
        self.stdout.write("✅ Bot ishga tushdi...")
        asyncio.run(main())

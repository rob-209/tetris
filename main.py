import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Импортируем из config - все работает как раньше
from config import BOT_TOKEN, BOARD_WIDTH, BOARD_HEIGHT, CELL_SIZE, BORDER, RECORDS_FILE, SHAPES, COLORS
from database.records import RecordsManager
from handlers.menu import MenuHandler
from handlers.records_handler import RecordsHandler
from handlers.game_handler import GameHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TetrisBot:
    def __init__(self):
        # Проверяем наличие BOT_TOKEN
        if not BOT_TOKEN:
            raise ValueError(
                "❌ BOT_TOKEN не найден!\n"
                "📝 Для локальной разработки:\n"
                "   - Создайте файл .env с BOT_TOKEN=ваш_токен\n"
                "   - Или установите переменную окружения\n\n"
                "🌐 Для деплоя на Render.com:\n"
                "   - Добавьте BOT_TOKEN в Environment Variables"
            )
        
        self.records_manager = RecordsManager()
        self.menu_handler = MenuHandler(self.records_manager)
        self.records_handler = RecordsHandler(self.records_manager)
        self.game_handler = GameHandler(self.records_manager)
        
        self.application = Application.builder().token(BOT_TOKEN).build()
        self._setup_handlers()
    
    # ... остальной код без изменений
    def _setup_handlers(self):
        """Настраивает обработчики команд"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help))
        self.application.add_handler(CommandHandler("play", self.play))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        await self.menu_handler.show_main_menu(update, context)
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        await update.message.reply_text(
            "🎮 **Команды бота:**\n\n"
            "/start - Главное меню\n"
            "/play - Начать игру\n"
            "/help - Справка\n\n"
            "Используйте кнопки для навигации!",
            parse_mode='Markdown'
        )
    
    async def play(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /play"""
        user = update.effective_user
        await self.game_handler.start_game(update, context, update.message, user)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик callback запросов"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        
        logger.info(f"Callback received: {query.data} from user {user.id}")
        
        # Всегда сначала проверяем меню и навигацию
        if query.data == "main_menu":
            await self.menu_handler.show_main_menu(update, context, query.message)
        
        elif query.data == "play_game":
            await self.game_handler.start_game(update, context, query.message, user)
        
        elif query.data == "show_records":
            await self.records_handler.show_records(update, context, query.message)
        
        elif query.data == "my_stats":
            await self.records_handler.show_user_stats(update, context, query.message, user)
        
        elif query.data == "show_rules":
            await self.menu_handler.show_rules(update, context, query.message)
        
        # Игровые действия передаем в game_handler
        elif query.data in ["left", "right", "down", "rotate", "drop", "end_game"]:
            await self.game_handler.handle_game_action(update, context, query, user)
        
        else:
            logger.warning(f"Unknown callback data: {query.data}")
            await query.message.reply_text("Неизвестная команда. Используйте кнопки меню.")
    
    def run(self):
        """Запускает бота"""
        print("🎮 Бот Тетрис запускается...")
        print("📱 Откройте Telegram и найдите своего бота")
        print("🚀 Отправьте /start для начала")
        
        self.application.run_polling()

if __name__ == '__main__':
    bot = TetrisBot()
    bot.run()
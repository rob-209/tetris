from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class MenuHandler:
    def __init__(self, records_manager):
        self.records_manager = records_manager
    
    async def show_main_menu(self, update, context, message=None):
        """Показывает главное меню"""
        keyboard = [
            [InlineKeyboardButton("🎮 Начать игру", callback_data="play_game")],
            [InlineKeyboardButton("🏆 Таблица рекордов", callback_data="show_records")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")],
            [InlineKeyboardButton("📖 Правила игры", callback_data="show_rules")]
        ]
        
        text = "🎯 **Главное меню Тетриса**\n\nВыберите действие:"
        
        if message:
            await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        else:
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def show_rules(self, update, context, message):
        """Показывает правила игры"""
        text = (
            "📖 **Правила Тетриса**\n\n"
            "🎯 **Цель игры:**\n"
            "• Заполняйте горизонтальные линии\n"
            "• Не допускайте заполнения верха\n\n"
            
            "🎮 **Управление:**\n"
            "⬅️/➡️ - Движение\n"
            "⬇️ - Ускорить падение\n"
            "🔄 - Поворот фигуры\n"
            "💥 - Мгновенное падение\n\n"
            
            "🏆 **Система очков:**\n"
            "• 1 линия = 100 очков\n"
            "• 2 линии = 300 очков\n" 
            "• 3 линии = 500 очков\n"
            "• 4 линии = 800 очков\n"
        )
        
        keyboard = [
            [InlineKeyboardButton("🎮 Начать игру", callback_data="play_game")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        
        await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
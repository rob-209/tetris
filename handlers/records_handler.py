from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

class RecordsHandler:
    def __init__(self, records_manager):
        self.records_manager = records_manager
    
    async def show_records(self, update, context, message):
        """Показывает таблицу рекордов"""
        top_records = self.records_manager.get_top_records(10)
        
        text = "🏆 **Топ-10 игроков**\n\n"
        
        if top_records:
            for i, record in enumerate(top_records, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                # Обрезаем длинные имена
                name = record['first_name']
                if len(name) > 15:
                    name = name[:15] + "..."
                text += f"{medal} {name} - **{record['score']}** очков\n"
        else:
            text += "🎯 Пока нет рекордов! Станьте первым!\n"
        
        text += f"\n👥 Всего игроков: {len(self.records_manager.records)}"
        
        keyboard = [
            [InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")],
            [InlineKeyboardButton("🎮 Начать игру", callback_data="play_game")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        
        try:
            await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        except Exception as e:
            # Если сообщение слишком длинное, упрощаем его
            simplified_text = "🏆 **Топ игроков**\n\nИспользуйте кнопки ниже для просмотра статистики:"
            await message.edit_text(simplified_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
    
    async def show_user_stats(self, update, context, message, user):
        """Показывает статистику пользователя"""
        stats = self.records_manager.get_user_stats(user.id)
        
        text = f"📊 **Статистика игрока** {user.first_name}\n\n"
        text += f"⭐ **Лучший результат:** **{stats['best_score']}** очков\n"
        text += f"🎯 **Последняя игра:** {stats['last_score']} очков\n"
        
        if stats['rank']:
            text += f"🏅 **Место в рейтинге:** {stats['rank']}\n"
        else:
            text += f"🏅 **Место в рейтинге:** не определено\n"
        
        text += f"🎮 **Сыграно игр:** {max(stats['games_played'], 1)}\n"
        text += f"👥 **Всего игроков:** {stats['total_players']}"
        
        if stats['best_score'] == 0:
            text += "\n\n🎯 У вас еще нет рекорда! Сыграйте первую игру!"
        
        keyboard = [
            [InlineKeyboardButton("🎮 Играть", callback_data="play_game")],
            [InlineKeyboardButton("🏆 Таблица рекордов", callback_data="show_records")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        
        try:
            await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        except Exception as e:
            # Упрощаем текст при ошибке
            simplified_text = f"📊 **Статистика** {user.first_name}\n\nЛучший результат: **{stats['best_score']}** очков"
            await message.edit_text(simplified_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
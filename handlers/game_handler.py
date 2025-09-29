from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import io
from game.tetris import TetrisGame
from game.renderer import GameRenderer

class GameHandler:
    def __init__(self, records_manager):
        self.records_manager = records_manager
        self.renderer = GameRenderer()
        self.games = {}
    
    async def handle_game_action(self, update, context, query, user):
        """Обработчик игровых действий"""
        # Игровые действия
        if query.data in ["left", "right", "down", "rotate", "drop", "end_game"]:
            await self._handle_game_actions(update, context, query, user)
    
    async def _handle_game_actions(self, update, context, query, user):
        """Обрабатывает игровые действия"""
        chat_id = query.message.chat_id
        
        if query.data == "end_game":
            # Удаляем игру и показываем меню завершения
            if chat_id in self.games:
                del self.games[chat_id]
            await self._show_game_over_menu(query, user)
            return
        
        if chat_id not in self.games:
            await self.start_game(update, context, query.message, user)
            return
        
        game = self.games[chat_id]
        
        # Игровая логика
        if query.data == "left": 
            game.move(-1, 0)
        elif query.data == "right": 
            game.move(1, 0)
        elif query.data == "down": 
            game.move(0, 1)
        elif query.data == "rotate": 
            game.rotate()
        elif query.data == "drop": 
            game.drop()
        
        if game.game_over:
            await self._show_game_over(query, user, game)
        else:
            await self._update_game_display(query, user, game)
    
    async def start_game(self, update, context, message, user):
        """Начинает новую игру"""
        chat_id = message.chat_id
        self.games[chat_id] = TetrisGame()
        await self._send_game_message(message, user)
    
    def _create_game_keyboard(self):
        """Создает игровую клавиатуру с кнопкой меню"""
        keyboard = [
            [
                InlineKeyboardButton("⬅️", callback_data="left"),
                InlineKeyboardButton("🔄", callback_data="rotate"),
                InlineKeyboardButton("➡️", callback_data="right")
            ],
            [
                InlineKeyboardButton("⬇️ Быстрее", callback_data="down"),
                InlineKeyboardButton("💨 Сбросить", callback_data="drop")
            ],
            [
                InlineKeyboardButton("⏹️ Завершить игру", callback_data="end_game")
            ],
            [
                InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")  # Добавлена кнопка меню
            ]
        ]
        return keyboard
    
    async def _send_game_message(self, message, user):
        """Отправляет игровое сообщение"""
        chat_id = message.chat_id
        game = self.games[chat_id]
        
        # Создаем изображение игры
        try:
            img = self.renderer.create_game_image(game)
            bio = io.BytesIO()
            img.save(bio, 'PNG')
            bio.seek(0)
            
            keyboard = self._create_game_keyboard()
            text = self._create_game_status_text(user, game)
            
            await message.reply_photo(
                photo=bio,
                caption=text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Ошибка создания изображения: {e}")
            # Если не удалось создать изображение, отправляем текстовую версию
            keyboard = self._create_game_keyboard()
            text = self._create_game_status_text(user, game) + "\n\n🖼️ Не удалось загрузить изображение игры"
            
            await message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
    
    async def _update_game_display(self, query, user, game):
        """Обновляет игровое сообщение"""
        try:
            # Пытаемся обновить как медиа (фото с подписью)
            img = self.renderer.create_game_image(game)
            bio = io.BytesIO()
            img.save(bio, 'PNG')
            bio.seek(0)
            
            keyboard = self._create_game_keyboard()
            text = self._create_game_status_text(user, game)
            
            await query.edit_message_media(
                media=InputMediaPhoto(media=bio, caption=text, parse_mode='Markdown'),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            print(f"Ошибка обновления медиа: {e}")
            # Если не удалось обновить медиа, пробуем обновить текст
            try:
                keyboard = self._create_game_keyboard()
                text = self._create_game_status_text(user, game) + "\n\n🖼️ Не удалось обновить изображение"
                
                await query.edit_message_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
            except Exception as e2:
                print(f"Ошибка обновления текста: {e2}")
                # Если и это не удалось, отправляем новое сообщение
                await self._send_game_message(query.message, user)
    
    async def _show_game_over(self, query, user, game):
        """Показывает экран окончания игры"""
        user_data = {'username': user.username, 'first_name': user.first_name}
        self.records_manager.update_record(user.id, user_data, game.score)
        
        # Удаляем игру
        chat_id = query.message.chat_id
        if chat_id in self.games:
            del self.games[chat_id]
        
        text = f"💀 **Игра окончена!**\n⭐ Очки: **{game.score}**"
        keyboard = [
            [InlineKeyboardButton("🎮 Новая игра", callback_data="play_game")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")],
            [InlineKeyboardButton("🏆 Таблица рекордов", callback_data="show_records")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        
        await self._safe_edit_message(query, text, keyboard)
    
    async def _show_game_over_menu(self, query, user):
        """Показывает меню после досрочного завершения игры"""
        chat_id = query.message.chat_id
        game = self.games.get(chat_id)
        score = game.score if game else 0
        
        if game:
            user_data = {'username': user.username, 'first_name': user.first_name}
            self.records_manager.update_record(user.id, user_data, score)
            if chat_id in self.games:
                del self.games[chat_id]
        
        text = f"⏹️ **Игра завершена**\n⭐ Набрано очков: **{score}**"
        keyboard = [
            [InlineKeyboardButton("🎮 Новая игра", callback_data="play_game")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")],
            [InlineKeyboardButton("🏆 Таблица рекордов", callback_data="show_records")],
            [InlineKeyboardButton("↩️ Главное меню", callback_data="main_menu")]
        ]
        
        await self._safe_edit_message(query, text, keyboard)
    
    def _create_game_status_text(self, user, game):
        """Создает текст статуса игры"""
        return f"🎮 **Игра Тетрис**\n👤 Игрок: {user.first_name}\n⭐ Очки: **{game.score}**\n📊 Уровень: **{game.level}**"
    
    async def _safe_edit_message(self, query, text, keyboard):
        """Безопасно редактирует сообщение с обработкой ошибок"""
        try:
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Ошибка редактирования сообщения: {e}")
            # Если не удалось отредактировать, отправляем новое сообщение
            await query.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
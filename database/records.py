import json
import os
from datetime import datetime
from config import RECORDS_FILE

class RecordsManager:
    def __init__(self):
        self.records = self._load_records()
    
    def _load_records(self):
        """Загружает рекорды из файла"""
        if os.path.exists(RECORDS_FILE):
            try:
                with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки рекордов: {e}")
                return {}
        return {}
    
    def _save_records(self):
        """Сохраняет рекорды в файл"""
        try:
            with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения рекордов: {e}")
    
    def update_record(self, user_id, user_data, score):
        """Обновляет рекорд пользователя"""
        user_id_str = str(user_id)
        current_time = datetime.now().isoformat()
        
        user_info = {
            'username': user_data.get('username', ''),
            'first_name': user_data.get('first_name', 'Игрок'),
            'last_name': user_data.get('last_name', ''),
            'score': score,
            'date': current_time,
            'last_played': current_time
        }
        
        is_new_record = False
        
        if user_id_str not in self.records:
            # Новый игрок
            self.records[user_id_str] = user_info
            is_new_record = True
        else:
            # Существующий игрок
            old_score = self.records[user_id_str].get('score', 0)
            if score > old_score:
                self.records[user_id_str].update(user_info)
                self.records[user_id_str]['best_score'] = score
                self.records[user_id_str]['best_date'] = current_time
                is_new_record = True
            else:
                # Обновляем только время последней игры
                self.records[user_id_str]['last_played'] = current_time
                self.records[user_id_str]['last_score'] = score
        
        self._save_records()
        return is_new_record
    
    def get_user_record(self, user_id):
        """Возвращает рекорд пользователя"""
        user_id_str = str(user_id)
        if user_id_str in self.records:
            record = self.records[user_id_str]
            return {
                'best_score': record.get('score', 0),
                'best_date': record.get('date', ''),
                'last_score': record.get('last_score', 0),
                'games_played': record.get('games_played', 1),
                'username': record.get('username', ''),
                'first_name': record.get('first_name', 'Игрок')
            }
        return {'best_score': 0, 'last_score': 0, 'games_played': 0, 'first_name': 'Игрок'}
    
    def get_top_records(self, limit=10):
        """Возвращает топ рекордов"""
        sorted_records = sorted(
            self.records.values(), 
            key=lambda x: x.get('score', 0), 
            reverse=True
        )[:limit]
        
        return [
            {
                'name': f"{r.get('first_name', 'Игрок')} ({r.get('username', '')})",
                'score': r.get('score', 0),
                'date': r.get('date', ''),
                'first_name': r.get('first_name', 'Игрок')
            }
            for r in sorted_records
        ]
    
    def get_user_stats(self, user_id):
        """Возвращает статистику пользователя"""
        user_record = self.get_user_record(user_id)
        top_records = self.get_top_records(100)  # Большой лимит для точного позиционирования
        
        user_rank = None
        for i, record in enumerate(top_records, 1):
            if record['score'] == user_record['best_score']:
                user_rank = i
                break
        
        return {
            **user_record,
            'rank': user_rank,
            'total_players': len(self.records)
        }
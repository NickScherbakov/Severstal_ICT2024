"""
TITAN Analytics Platform - Data Processors Registry
Система обработчиков данных для различных типов аналитики
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json


class DataProcessor(ABC):
    """Базовый класс для обработчиков данных"""
    
    @abstractmethod
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        """Проверяет, может ли обработчик работать с этим типом данных"""
        pass
    
    @abstractmethod
    def process(self, data: Any, params: Dict) -> Dict:
        """Обрабатывает данные и возвращает представление"""
        pass
    
    def get_name(self) -> str:
        """Возвращает название обработчика"""
        return self.__class__.__name__


class ProcessorRegistry:
    """Реестр обработчиков данных"""
    _processors: List[DataProcessor] = []
    _initialized = False
    
    @classmethod
    def register(cls, processor: DataProcessor):
        """Регистрирует новый обработчик"""
        if processor not in cls._processors:
            cls._processors.append(processor)
            print(f"✅ Registered processor: {processor.get_name()}")
    
    @classmethod
    def get_processor(cls, block_type: str, data_type: str = 'text') -> Optional[DataProcessor]:
        """Находит подходящий обработчик"""
        for processor in cls._processors:
            if processor.can_process(block_type, data_type):
                return processor
        return None
    
    @classmethod
    def list_processors(cls) -> List[str]:
        """Возвращает список зарегистрированных обработчиков"""
        return [p.get_name() for p in cls._processors]
    
    @classmethod
    def initialize(cls):
        """Инициализирует все базовые обработчики"""
        if cls._initialized:
            return
        
        cls.register(SentimentAnalysisProcessor())
        cls.register(NetworkGraphProcessor())
        cls.register(TimelineProcessor())
        cls.register(ComparisonProcessor())
        cls.register(ForecastProcessor())
        cls.register(TableProcessor())
        
        cls._initialized = True
        print(f"🚀 TITAN Analytics: Initialized {len(cls._processors)} processors")


class SentimentAnalysisProcessor(DataProcessor):
    """Анализ тональности текста с использованием YandexGPT"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'sentiment'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Анализирует тональность текста
        
        Args:
            data: текстовые данные для анализа
            params: параметры обработки (model, detailed и т.д.)
        
        Returns:
            Dict с результатами анализа тональности
        """
        from search.yagpt import ask_yagpt
        from analyst.settings import YANDEX_SEARCH_API_TOKEN
        
        # Проверяем наличие данных
        if not data or (isinstance(data, dict) and not data.get('data')):
            return {
                'type': 'sentiment',
                'error': 'Нет данных для анализа'
            }
        
        # Извлекаем текст
        text = data.get('data') if isinstance(data, dict) else str(data)
        
        # Формируем промпт
        prompt = f"""Проанализируй тональность следующего текста.

Определи:
1. Общая тональность: позитивная, негативная или нейтральная
2. Уровень эмоциональности (от 1 до 10)
3. Ключевые эмоции
4. Основные причины такой тональности

Представь результат в JSON формате:
{{
  "sentiment": "positive|negative|neutral",
  "score": 0-10,
  "emotions": ["эмоция1", "эмоция2"],
  "reasons": ["причина1", "причина2"],
  "summary": "краткое резюме"
}}

Текст: {text[:2000]}"""
        
        try:
            result = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                params.get('model', 'yandexgpt')
            )
            
            # Пытаемся распарсить JSON
            try:
                analysis = json.loads(result)
            except json.JSONDecodeError:
                # Если не JSON, сохраняем как есть
                analysis = {'summary': result}
            
            return {
                'type': 'sentiment',
                'analysis': analysis,
                'raw_text': result,
                'visualization': {
                    'type': 'sentiment_gauge',
                    'value': analysis.get('score', 5) if isinstance(analysis, dict) else 5,
                    'sentiment': analysis.get('sentiment', 'neutral') if isinstance(analysis, dict) else 'neutral'
                }
            }
        except Exception as e:
            return {
                'type': 'sentiment',
                'error': f'Ошибка анализа: {str(e)}'
            }


class NetworkGraphProcessor(DataProcessor):
    """Построение графа связей между сущностями"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'network'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Строит граф связей между упоминаемыми сущностями
        """
        from search.yagpt import ask_yagpt
        from analyst.settings import YANDEX_SEARCH_API_TOKEN
        
        if not data or (isinstance(data, dict) and not data.get('data')):
            return {
                'type': 'network',
                'error': 'Нет данных для анализа'
            }
        
        text = data.get('data') if isinstance(data, dict) else str(data)
        
        prompt = f"""Извлеки из текста все важные сущности (организации, люди, события) и связи между ними.

Верни результат в JSON формате:
{{
  "nodes": [
    {{"id": "node1", "label": "Название", "type": "organization|person|event"}},
    {{"id": "node2", "label": "Название", "type": "organization|person|event"}}
  ],
  "edges": [
    {{"from": "node1", "to": "node2", "label": "тип связи", "weight": 1-10}}
  ]
}}

Текст: {text[:2000]}"""
        
        try:
            result = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                params.get('model', 'yandexgpt')
            )
            
            try:
                graph_data = json.loads(result)
            except json.JSONDecodeError:
                # Fallback: создаём простой граф
                graph_data = {
                    'nodes': [{'id': '1', 'label': 'Данные', 'type': 'data'}],
                    'edges': []
                }
            
            return {
                'type': 'network',
                'graph_data': graph_data,
                'visualization': 'cytoscape',
                'raw_text': result
            }
        except Exception as e:
            return {
                'type': 'network',
                'error': f'Ошибка построения графа: {str(e)}'
            }


class TimelineProcessor(DataProcessor):
    """Построение временной шкалы событий"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'timeline'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Извлекает события с датами и строит временную шкалу
        """
        from search.yagpt import ask_yagpt
        from analyst.settings import YANDEX_SEARCH_API_TOKEN
        
        if not data or (isinstance(data, dict) and not data.get('data')):
            return {
                'type': 'timeline',
                'error': 'Нет данных для анализа'
            }
        
        text = data.get('data') if isinstance(data, dict) else str(data)
        
        prompt = f"""Извлеки из текста все упоминания событий с датами.

Верни результат в JSON формате:
{{
  "events": [
    {{
      "date": "YYYY-MM-DD",
      "title": "Краткое название события",
      "description": "Описание",
      "importance": 1-10
    }}
  ]
}}

Если точная дата неизвестна, используй приблизительную или "unknown".

Текст: {text[:2000]}"""
        
        try:
            result = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                params.get('model', 'yandexgpt')
            )
            
            try:
                timeline_data = json.loads(result)
            except json.JSONDecodeError:
                timeline_data = {'events': []}
            
            return {
                'type': 'timeline',
                'timeline_data': timeline_data,
                'visualization': 'timeline',
                'raw_text': result
            }
        except Exception as e:
            return {
                'type': 'timeline',
                'error': f'Ошибка построения таймлайна: {str(e)}'
            }


class ComparisonProcessor(DataProcessor):
    """Сравнительный анализ данных"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'comparison'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Выполняет сравнительный анализ
        """
        from search.yagpt import ask_yagpt
        from analyst.settings import YANDEX_SEARCH_API_TOKEN
        
        if not data or (isinstance(data, dict) and not data.get('data')):
            return {
                'type': 'comparison',
                'error': 'Нет данных для анализа'
            }
        
        text = data.get('data') if isinstance(data, dict) else str(data)
        comparison_items = params.get('items', [])
        
        if comparison_items:
            prompt = f"""Сравни следующие аспекты: {', '.join(comparison_items)}

На основе текста:
{text[:2000]}

Верни результат в JSON формате:
{{
  "comparison": [
    {{
      "item": "название аспекта",
      "value": "значение/описание",
      "score": 1-10
    }}
  ],
  "summary": "общий вывод из сравнения"
}}"""
        else:
            prompt = f"""Проведи сравнительный анализ информации в тексте.
Выдели ключевые аспекты для сравнения.

Текст: {text[:2000]}

Верни результат в JSON формате с comparison массивом."""
        
        try:
            result = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                params.get('model', 'yandexgpt')
            )
            
            try:
                comparison_data = json.loads(result)
            except json.JSONDecodeError:
                comparison_data = {'summary': result}
            
            return {
                'type': 'comparison',
                'comparison_data': comparison_data,
                'visualization': 'radar_chart',
                'raw_text': result
            }
        except Exception as e:
            return {
                'type': 'comparison',
                'error': f'Ошибка сравнения: {str(e)}'
            }


class ForecastProcessor(DataProcessor):
    """Прогнозирование на основе данных"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'forecast'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Генерирует прогноз на основе данных
        """
        from search.yagpt import ask_yagpt
        from analyst.settings import YANDEX_SEARCH_API_TOKEN
        
        if not data or (isinstance(data, dict) and not data.get('data')):
            return {
                'type': 'forecast',
                'error': 'Нет данных для анализа'
            }
        
        text = data.get('data') if isinstance(data, dict) else str(data)
        
        prompt = f"""На основе представленной информации сделай прогноз развития ситуации.

Информация:
{text[:2000]}

Верни результат в JSON формате:
{{
  "forecast": {{
    "short_term": "прогноз на ближайшую перспективу",
    "medium_term": "прогноз на среднюю перспективу",
    "long_term": "прогноз на долгую перспективу"
  }},
  "scenarios": [
    {{
      "name": "название сценария",
      "probability": 0-100,
      "description": "описание"
    }}
  ],
  "risks": ["риск1", "риск2"],
  "opportunities": ["возможность1", "возможность2"]
}}"""
        
        try:
            result = ask_yagpt(
                prompt,
                YANDEX_SEARCH_API_TOKEN,
                params.get('model', 'yandexgpt')
            )
            
            try:
                forecast_data = json.loads(result)
            except json.JSONDecodeError:
                forecast_data = {'forecast': {'summary': result}}
            
            return {
                'type': 'forecast',
                'forecast_data': forecast_data,
                'visualization': 'forecast_chart',
                'raw_text': result
            }
        except Exception as e:
            return {
                'type': 'forecast',
                'error': f'Ошибка прогнозирования: {str(e)}'
            }


class TableProcessor(DataProcessor):
    """Обработка табличных данных"""
    
    def can_process(self, block_type: str, data_type: str = 'text') -> bool:
        return block_type == 'table'
    
    def process(self, data: Any, params: Dict) -> Dict:
        """
        Извлекает и форматирует табличные данные
        """
        if not data:
            return {
                'type': 'table',
                'error': 'Нет данных для отображения'
            }
        
        # Если данные уже в табличном формате
        if isinstance(data, dict) and 'data' in data:
            table_data = data['data']
            
            # Проверяем, является ли это уже таблицей
            if isinstance(table_data, list) and len(table_data) > 0:
                return {
                    'type': 'table',
                    'table_data': {
                        'headers': list(table_data[0].keys()) if isinstance(table_data[0], dict) else [],
                        'rows': table_data
                    },
                    'visualization': 'table'
                }
        
        # Иначе просто возвращаем данные как есть
        return {
            'type': 'table',
            'table_data': data,
            'visualization': 'table'
        }


# Автоматическая инициализация при импорте модуля
ProcessorRegistry.initialize()

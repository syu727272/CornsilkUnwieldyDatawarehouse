"""
データモデルモジュール
アプリケーションで使用するデータモデルを定義
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class DataPoint:
    """
    データポイントを表すデータクラス
    
    Attributes:
        timestamp (datetime): データのタイムスタンプ
        value (float): 測定値
        category (str): データのカテゴリ
        metadata (dict): 追加のメタデータ
    """
    timestamp: datetime
    value: float
    category: str
    metadata: Optional[dict] = None

class DataSet:
    """
    データセットを管理するクラス
    """
    def __init__(self):
        self._data: List[DataPoint] = []
    
    def add_data_point(self, data_point: DataPoint) -> None:
        """
        データポイントを追加
        
        Args:
            data_point (DataPoint): 追加するデータポイント
        """
        self._data.append(data_point)
    
    def get_data(self) -> List[DataPoint]:
        """
        全データポイントを取得
        
        Returns:
            List[DataPoint]: データポイントのリスト
        """
        return self._data.copy()
    
    def filter_by_category(self, category: str) -> List[DataPoint]:
        """
        カテゴリでフィルタリングしたデータを取得
        
        Args:
            category (str): フィルタリングするカテゴリ
            
        Returns:
            List[DataPoint]: フィルタリングされたデータポイントのリスト
        """
        return [d for d in self._data if d.category == category]

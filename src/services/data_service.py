"""
データサービスモジュール
データの処理と分析を行うビジネスロジックを提供
"""
import pandas as pd
from typing import List, Dict, Any
from src.models.data_model import DataSet, DataPoint

class DataService:
    """
    データ処理と分析のためのサービスクラス
    """
    def __init__(self):
        self._dataset = DataSet()
    
    def process_data(self, raw_data: pd.DataFrame) -> None:
        """
        生データを処理してデータセットに追加
        
        Args:
            raw_data (pd.DataFrame): 処理する生データ
        """
        # データの前処理と検証
        processed_data = self._preprocess_data(raw_data)
        
        # データセットに追加
        for _, row in processed_data.iterrows():
            data_point = DataPoint(
                timestamp=row['timestamp'],
                value=row['value'],
                category=row['category']
            )
            self._dataset.add_data_point(data_point)
    
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        データの前処理を実行
        
        Args:
            data (pd.DataFrame): 前処理する生データ
            
        Returns:
            pd.DataFrame: 前処理済みデータ
        """
        # 欠損値の処理
        processed = data.copy()
        processed = processed.dropna()
        
        # データ型の変換と検証
        processed['timestamp'] = pd.to_datetime(processed['timestamp'])
        processed['value'] = pd.to_numeric(processed['value'])
        
        return processed
    
    def get_analysis_results(self) -> Dict[str, Any]:
        """
        データ分析結果を取得
        
        Returns:
            Dict[str, Any]: 分析結果を含む辞書
        """
        data_points = self._dataset.get_data()
        
        if not data_points:
            return {"error": "データが存在しません"}
        
        # 基本的な統計情報を計算
        values = [dp.value for dp in data_points]
        categories = set(dp.category for dp in data_points)
        
        results = {
            "total_points": len(data_points),
            "categories": list(categories),
            "statistics": {
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
        }
        
        return results

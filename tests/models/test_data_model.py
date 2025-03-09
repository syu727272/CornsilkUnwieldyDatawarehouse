"""
データモデルのテストモジュール
"""
from datetime import datetime
import pytest
from src.models.data_model import DataPoint, DataSet

def test_data_point_creation():
    """データポイントの作成テスト"""
    timestamp = datetime.now()
    data_point = DataPoint(
        timestamp=timestamp,
        value=10.5,
        category="test"
    )
    
    assert data_point.timestamp == timestamp
    assert data_point.value == 10.5
    assert data_point.category == "test"
    assert data_point.metadata is None

def test_dataset_add_and_get_data():
    """データセットへのデータ追加と取得テスト"""
    dataset = DataSet()
    data_point = DataPoint(
        timestamp=datetime.now(),
        value=15.0,
        category="test"
    )
    
    dataset.add_data_point(data_point)
    data = dataset.get_data()
    
    assert len(data) == 1
    assert data[0] == data_point

def test_dataset_filter_by_category():
    """カテゴリによるフィルタリングテスト"""
    dataset = DataSet()
    
    # 異なるカテゴリのデータポイントを追加
    dp1 = DataPoint(datetime.now(), 10.0, "cat1")
    dp2 = DataPoint(datetime.now(), 20.0, "cat2")
    dp3 = DataPoint(datetime.now(), 30.0, "cat1")
    
    dataset.add_data_point(dp1)
    dataset.add_data_point(dp2)
    dataset.add_data_point(dp3)
    
    # フィルタリングテスト
    cat1_data = dataset.filter_by_category("cat1")
    assert len(cat1_data) == 2
    assert all(dp.category == "cat1" for dp in cat1_data)

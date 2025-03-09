"""
データサービスのテストモジュール
"""
import pandas as pd
import pytest
from datetime import datetime
from src.services.data_service import DataService

@pytest.fixture
def data_service():
    """DataServiceのフィクスチャ"""
    return DataService()

@pytest.fixture
def sample_dataframe():
    """テスト用のサンプルDataFrame"""
    return pd.DataFrame({
        'timestamp': ['2024-01-01', '2024-01-02', '2024-01-03'],
        'value': [10.0, 20.0, 30.0],
        'category': ['A', 'B', 'A']
    })

def test_process_data(data_service, sample_dataframe):
    """データ処理のテスト"""
    # データ処理の実行
    data_service.process_data(sample_dataframe)
    
    # 分析結果の取得と検証
    results = data_service.get_analysis_results()
    
    assert results['total_points'] == 3
    assert set(results['categories']) == {'A', 'B'}
    assert results['statistics']['mean'] == 20.0
    assert results['statistics']['min'] == 10.0
    assert results['statistics']['max'] == 30.0

def test_process_data_with_missing_values(data_service):
    """欠損値を含むデータ処理のテスト"""
    df_with_na = pd.DataFrame({
        'timestamp': ['2024-01-01', '2024-01-02', None],
        'value': [10.0, None, 30.0],
        'category': ['A', 'B', 'A']
    })
    
    # データ処理の実行
    data_service.process_data(df_with_na)
    
    # 分析結果の検証（欠損値は除外されているはず）
    results = data_service.get_analysis_results()
    assert results['total_points'] == 1  # 完全なデータポイントは1つだけ

def test_empty_dataset(data_service):
    """空のデータセットの処理テスト"""
    results = data_service.get_analysis_results()
    assert "error" in results
    assert results["error"] == "データが存在しません"

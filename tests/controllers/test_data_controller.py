"""
データコントローラーのテストモジュール
"""
import pytest
import pandas as pd
import streamlit as st
from unittest.mock import MagicMock, patch
from src.controllers.data_controller import DataController
from src.services.data_service import DataService

@pytest.fixture
def data_service():
    """DataServiceのモックフィクスチャ"""
    return MagicMock(spec=DataService)

@pytest.fixture
def data_controller(data_service):
    """DataControllerのフィクスチャ"""
    return DataController(data_service)

def test_display_analysis_results_success(data_controller, data_service):
    """分析結果の表示テスト（正常系）"""
    # モックデータの準備
    mock_results = {
        "total_points": 100,
        "categories": ["A", "B", "C"],
        "statistics": {
            "mean": 50.0,
            "min": 10.0,
            "max": 90.0
        }
    }
    data_service.get_analysis_results.return_value = mock_results
    
    # streamlitのモック化
    with patch("streamlit.metric") as mock_metric:
        with patch("streamlit.write") as mock_write:
            data_controller.display_analysis_results()
            
            # メトリクスの表示確認
            mock_metric.assert_any_call("データポイント数", 100)
            mock_metric.assert_any_call("平均値", "50.00")
            mock_metric.assert_any_call("最小値", "10.00")
            mock_metric.assert_any_call("最大値", "90.00")

def test_display_analysis_results_error(data_controller, data_service):
    """分析結果の表示テスト（エラー系）"""
    # エラーケースのモックデータ
    mock_results = {"error": "データが存在しません"}
    data_service.get_analysis_results.return_value = mock_results
    
    # streamlitのモック化
    with patch("streamlit.warning") as mock_warning:
        data_controller.display_analysis_results()
        mock_warning.assert_called_once_with("データが存在しません")

def test_show_data_filters(data_controller, data_service):
    """データフィルター表示のテスト"""
    # モックデータの準備
    mock_results = {
        "categories": ["カテゴリA", "カテゴリB"]
    }
    data_service.get_analysis_results.return_value = mock_results
    
    # streamlitのモック化
    with patch("streamlit.selectbox") as mock_selectbox:
        data_controller.show_data_filters()
        
        # セレクトボックスの表示確認
        mock_selectbox.assert_called_once_with(
            "カテゴリ選択",
            options=["全て", "カテゴリA", "カテゴリB"]
        )

"""
データコントローラーモジュール
UIとビジネスロジック間の橋渡しを行う
"""
import streamlit as st
import pandas as pd
from src.services.data_service import DataService

class DataController:
    """
    データ処理と表示を制御するコントローラークラス
    """
    def __init__(self, data_service: DataService):
        """
        コントローラーの初期化
        
        Args:
            data_service (DataService): データ処理サービス
        """
        self._service = data_service
    
    def handle_file_upload(self) -> None:
        """
        ファイルアップロードの処理を行う
        """
        uploaded_file = st.file_uploader(
            "データファイルをアップロード (CSV)",
            type=['csv']
        )
        
        if uploaded_file is not None:
            try:
                # データの読み込みと処理
                df = pd.read_csv(uploaded_file)
                self._service.process_data(df)
                st.success("データを正常に読み込みました")
                
                # 分析結果の表示
                self.display_analysis_results()
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
    
    def display_analysis_results(self) -> None:
        """
        分析結果を画面に表示
        """
        results = self._service.get_analysis_results()
        
        if "error" in results:
            st.warning(results["error"])
            return
        
        # 基本情報の表示
        st.subheader("基本情報")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("データポイント数", results["total_points"])
            st.write("カテゴリ一覧:", ", ".join(results["categories"]))
        
        with col2:
            stats = results["statistics"]
            st.metric("平均値", f"{stats['mean']:.2f}")
            st.metric("最小値", f"{stats['min']:.2f}")
            st.metric("最大値", f"{stats['max']:.2f}")
    
    def show_data_filters(self) -> None:
        """
        データフィルタリングのUIを表示
        """
        with st.sidebar:
            st.subheader("フィルター設定")
            # フィルタリングオプションを追加
            results = self._service.get_analysis_results()
            if "categories" in results:
                selected_category = st.selectbox(
                    "カテゴリ選択",
                    options=["全て"] + results["categories"]
                )
                # フィルタリングロジックをここに実装

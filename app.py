import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="ストリートファイターリーグ管理",
    page_icon="🥊",
    layout="wide"
)

# データベース初期化
def init_database():
    conn = sqlite3.connect('league.db')
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            game_date TIMESTAMP,
            home_score INTEGER DEFAULT 0,
            away_score INTEGER DEFAULT 0,
            FOREIGN KEY (home_team_id) REFERENCES teams (id),
            FOREIGN KEY (away_team_id) REFERENCES teams (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            match_type TEXT NOT NULL,
            home_player TEXT,
            away_player TEXT,
            home_sets INTEGER DEFAULT 0,
            away_sets INTEGER DEFAULT 0,
            winner TEXT,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES games (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# メインアプリケーション
def main():
    st.title("🥊 ストリートファイターリーグ管理システム")
    
    # データベース初期化
    init_database()
    
    # サイドバー
    st.sidebar.title("メニュー")
    page = st.sidebar.selectbox(
        "ページを選択",
        ["🏠 ダッシュボード", "👥 チーム管理", "🎮 試合管理", "📊 統計・分析"]
    )
    
    if page == "🏠 ダッシュボード":
        show_dashboard()
    elif page == "👥 チーム管理":
        show_team_management()
    elif page == "🎮 試合管理":
        show_game_management()
    elif page == "📊 統計・分析":
        show_statistics()

def show_dashboard():
    st.header("📊 ダッシュボード")
    
    # 基本統計
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("参加チーム数", "0")
    
    with col2:
        st.metric("総試合数", "0")
    
    with col3:
        st.metric("完了試合数", "0")
    
    with col4:
        st.metric("残り試合数", "0")
    
    # 順位表（プレースホルダー）
    st.subheader("🏆 順位表")
    st.info("チームと試合データを登録すると、ここに順位表が表示されます。")

def show_team_management():
    st.header("👥 チーム管理")
    
    # チーム登録フォーム
    with st.form("team_registration"):
        st.subheader("新規チーム登録")
        
        team_name = st.text_input("チーム名", placeholder="例：格闘家集団")
        
        st.subheader("メンバー情報")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**先鋒**")
            vanguard = st.text_input("先鋒プレイヤー名", key="vanguard")
            
            st.write("**中堅**")
            middle = st.text_input("中堅プレイヤー名", key="middle")
        
        with col2:
            st.write("**大将**")
            captain = st.text_input("大将プレイヤー名", key="captain")
            
            st.write("**控え**")
            substitute = st.text_input("控えプレイヤー名", key="substitute")
        
        if st.form_submit_button("チーム登録"):
            if team_name and vanguard and middle and captain and substitute:
                # データベースに保存
                conn = sqlite3.connect('league.db')
                cursor = conn.cursor()
                
                try:
                    # チーム登録
                    cursor.execute("INSERT INTO teams (name) VALUES (?)", (team_name,))
                    team_id = cursor.lastrowid
                    
                    # プレイヤー登録
                    players = [
                        (team_id, vanguard, "先鋒"),
                        (team_id, middle, "中堅"),
                        (team_id, captain, "大将"),
                        (team_id, substitute, "控え")
                    ]
                    
                    cursor.executemany(
                        "INSERT INTO players (team_id, name, role) VALUES (?, ?, ?)",
                        players
                    )
                    
                    conn.commit()
                    st.success(f"チーム「{team_name}」を登録しました！")
                    
                except sqlite3.IntegrityError:
                    st.error("このチーム名は既に登録されています。")
                finally:
                    conn.close()
            else:
                st.error("すべての項目を入力してください。")
    
    # 登録済みチーム一覧
    st.subheader("登録済みチーム")
    conn = sqlite3.connect('league.db')
    teams_df = pd.read_sql_query("SELECT * FROM teams", conn)
    conn.close()
    
    if not teams_df.empty:
        st.dataframe(teams_df)
    else:
        st.info("まだチームが登録されていません。")

def show_game_management():
    st.header("🎮 試合管理")
    st.info("試合管理機能は開発中です。")

def show_statistics():
    st.header("📊 統計・分析")
    st.info("統計・分析機能は開発中です。")

if __name__ == "__main__":
    main()

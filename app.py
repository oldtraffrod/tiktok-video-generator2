import streamlit as st
import os
import time
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from media_search import MediaSearch
from video_generator import VideoGenerator

# NLTKデータのダウンロード（初回実行時のみ）
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# ディレクトリの作成
os.makedirs('media', exist_ok=True)
os.makedirs('output', exist_ok=True)
os.makedirs('audio', exist_ok=True)

# セッション状態の初期化
if 'scenes' not in st.session_state:
    st.session_state.scenes = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'media_dict' not in st.session_state:
    st.session_state.media_dict = {}
if 'generated_video' not in st.session_state:
    st.session_state.generated_video = None

# メディア検索クラスのインスタンス化
media_search = MediaSearch()

# 動画生成クラスのインスタンス化
video_generator = VideoGenerator()

# アプリのタイトル
st.title("TikTok動画生成ツール")

# シンプルなカスタムCSS
st.markdown("""
<style>
.main {
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ステップ表示
steps = ["1. 台本入力", "2. メディア選択", "3. 動画生成", "4. 動画出力"]
st.progress((st.session_state.current_step - 1) / (len(steps) - 1))
st.write(f"**現在のステップ: {steps[st.session_state.current_step - 1]}**")

# 台本からキーワードを抽出する関数
def extract_keywords(text, max_keywords=5):
    # テキストを小文字に変換し、トークン化
    tokens = word_tokenize(text.lower())
    
    # ストップワードを除去
    stop_words = set(stopwords.words('english'))
    try:
        stop_words.update(set(stopwords.words('japanese')))
    except:
        pass
    
    # 一般的なストップワードを追加
    custom_stop_words = {'の', 'に', 'は', 'を', 'た', 'が', 'で', 'て', 'と', 'し', 'れ', 'さ', 'ある', 'いる', 'する', 'ない', 'れる', 'られ', 'なる', 'よう', 'こと', 'もの', 'これ', 'それ', 'あれ', 'どれ'}
    stop_words.update(custom_stop_words)
    
    filtered_tokens = [token for token in tokens if token not in stop_words and token.isalnum() and len(token) > 1]
    
    # 単語の出現回数をカウント
    word_freq = {}
    for token in filtered_tokens:
        if token in word_freq:
            word_freq[token] += 1
        else:
            word_freq[token] = 1
    
    # 出現回数で並べ替えて上位のキーワードを取得
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return keywords

# 台本を解析してシーンに分割する関数
def parse_script(script_text):
    scenes = {}
    scene_texts = [scene.strip() for scene in script_text.split('\n\n') if scene.strip()]
    
    for i, scene_text in enumerate(scene_texts):
        scene_id = f"scene_{i+1}"
        keywords = extract_keywords(scene_text)
        scenes[scene_id] = {
            "text": scene_text,
            "keywords": keywords
        }
    
    return scenes

# ステップ1: 台本入力
if st.session_state.current_step == 1:
    st.header("台本入力")
    
    st.write("TikTokで使用する台本を入力してください。各シーンは空行で区切ってください。")
    
    # サンプル台本
    if st.button("サンプル台本（料理レシピ）"):
        sample_script = """今日は簡単で美味しい塩レモンパスタの作り方をご紹介します。

材料は、パスタ、レモン、オリーブオイル、塩、黒胡椒、パルメザンチーズです。

まず、お湯を沸かしてパスタを表示時間通りに茹でます。

レモンの皮をすりおろし、果汁を絞っておきます。

パスタが茹で上がったら、オリーブオイル、レモンの皮と果汁、塩を加えて和えます。

最後に黒胡椒とパルメザンチーズをかけて完成です。

簡単なのに爽やかで美味しい塩レモンパスタ、ぜひ試してみてください！"""
        st.session_state.script_text = sample_script
    
    if st.button("サンプル台本（旅行紹介）"):
        sample_script = """京都の魅力を60秒でご紹介します！

まず訪れたいのは金閣寺。美しい金箔に覆われた建物が池に映る姿は圧巻です。

次は嵐山の竹林。風に揺れる竹の音を聞きながら散策するのがおすすめです。

お昼は京都名物の湯葉料理。繊細な味わいが京都らしさを感じさせます。

午後は清水寺へ。舞台から見る京都の街並みは絶景です。

夕方は祇園で舞妓さんを探しながら散策。風情ある町家が並ぶ景色も素敵です。

最後は夜の伏見稲荷大社。赤い鳥居のトンネルがライトアップされて幻想的です。

京都は四季折々の表情があるので、ぜひ何度も訪れてみてください！"""
        st.session_state.script_text = sample_script
    
    script_text = st.text_area("台本を入力", height=300, key="script_text")
    
    if st.button("台本を解析"):
        if script_text:
            # 台本を解析してシーンに分割
            st.session_state.scenes = parse_script(script_text)
            st.session_state.current_step = 2
            st.experimental_rerun()
        else:
            st.error("台本を入力してください。")

# ステップ2: メディア選択
elif st.session_state.current_step == 2:
    st.header("メディア選択")
    
    st.write("各シーンに使用する画像や動画を選択してください。")
    
    # 各シーンごとにメディア選択
    all_scenes_have_media = True
    
    for scene_id, scene_data in st.session_state.scenes.items():
        st.subheader(f"シーン {scene_id.split('_')[1]}")
        st.write(scene_data["text"])
        
        # シーンのメディア辞書を初期化
        if scene_id not in st.session_state.media_dict:
            st.session_state.media_dict[scene_id] = []
        
        # キーワードボタン
        st.write("キーワードをクリックして画像を検索:")
        keyword_cols = st.columns(len(scene_data["keywords"]) + 1)
        
        for i, keyword in enumerate(scene_data["keywords"]):
            if keyword_cols[i].button(keyword, key=f"{scene_id}_{keyword}"):
                st.session_state.current_search_scene = scene_id
                st.session_state.current_search_keyword = keyword
        
        # カスタムキーワード検索
        with keyword_cols[-1]:
            if st.button("カスタム検索", key=f"{scene_id}_custom"):
                st.session_state.current_search_scene = scene_id
                st.session_state.current_search_keyword = None
        
        # 検索キーワード入力
        if hasattr(st.session_state, 'current_search_scene') and st.session_state.current_search_scene == scene_id:
            search_keyword = st.session_state.current_search_keyword
            if search_keyword is None:
                search_keyword = st.text_input("検索キーワードを入力:", key=f"{scene_id}_search_input")
            
            if search_keyword:
                with st.spinner(f"「{search_keyword}」の画像を検索中..."):
                    # 画像検索
                    search_results = media_search.search_images(search_keyword, max_results=9)
                    
                    if search_results:
                        st.write(f"{len(search_results)}件の画像が見つかりました:")
                        
                        # 画像を3列で表示
                        cols = st.columns(3)
                        for i, result in enumerate(search_results):
                            with cols[i % 3]:
                                st.image(result["thumbnail_url"], caption=result.get("title", ""), use_column_width=True)
                                if st.button("選択", key=f"{scene_id}_{i}_select"):
                                    # 画像をダウンロード
                                    local_path = media_search.download_media(result["url"], f"media/{scene_id}_{int(time.time())}_{i}.jpg")
                                    if local_path:
                                        # メディア情報を保存
                                        media_info = {
                                            "id": f"{scene_id}_{i}",
                                            "keyword": search_keyword,
                                            "url": result["url"],
                                            "local_path": local_path,
                                            "type": "image"
                                        }
                                        st.session_state.media_dict[scene_id].append(media_info)
                                        st.success(f"画像を選択しました！")
                                        # 検索状態をリセット
                                        if hasattr(st.session_state, 'current_search_scene'):
                                            delattr(st.session_state, 'current_search_scene')
                                        if hasattr(st.session_state, 'current_search_keyword'):
                                            delattr(st.session_state, 'current_search_keyword')
                                        st.experimental_rerun()
                    else:
                        st.warning("画像が見つかりませんでした。別のキーワードで試してください。")
        
        # 選択したメディアの表示
        if st.session_state.media_dict[scene_id]:
            st.write("選択したメディア:")
            media_cols = st.columns(min(3, len(st.session_state.media_dict[scene_id])))
            
            for i, media_info in enumerate(st.session_state.media_dict[scene_id]):
                with media_cols[i % 3]:
                    st.image(media_info["local_path"], caption=media_info["keyword"], use_column_width=True)
                    if st.button("削除", key=f"{scene_id}_{i}_remove"):
                        # メディアを削除
                        st.session_state.media_dict[scene_id].remove(media_info)
                        st.experimental_rerun()
        else:
            st.warning("このシーンにはまだメディアが選択されていません。")
            all_scenes_have_media = False
        
        st.markdown("---")
    
    # 次のステップへ
    col1, col2 = st.columns(2)
    with col1:
        if st.button("前のステップへ戻る"):
            st.session_state.current_step = 1
            st.experimental_rerun()
    
    with col2:
        if st.button("次へ進む", disabled=not all_scenes_have_media):
            if all_scenes_have_media:
                st.session_state.current_step = 3
                st.experimental_rerun()
            else:
                st.error("すべてのシーンに少なくとも1つのメディアを選択してください。")

# ステップ3: 動画生成
elif st.session_state.current_step == 3:
    st.header("動画生成")
    
    st.write("選択したメディアを使って動画を生成します。")
    
    # シーンとメディアの確認
    st.subheader("シーンとメディアの確認")
    for scene_id, scene_data in st.session_state.scenes.items():
        with st.expander(f"シーン {scene_id.split('_')[1]}: {scene_data['text'][:50]}..."):
            st.write(scene_data["text"])
            
            if scene_id in st.session_state.media_dict and st.session_state.media_dict[scene_id]:
                media_cols = st.columns(min(3, len(st.session_state.media_dict[scene_id])))
                for i, media_info in enumerate(st.session_state.media_dict[scene_id]):
                    with media_cols[i % 3]:
                        st.image(media_info["local_path"], caption=media_info["keyword"], use_column_width=True)
            else:
                st.warning("このシーンにはメディアが選択されていません。")
    
    # 動画生成オプション
    st.subheader("動画生成オプション")
    
    col1, col2 = st.columns(2)
    with col1:
        scene_duration = st.slider("シーンあたりの秒数", min_value=3, max_value=10, value=5, step=1)
        add_title = st.checkbox("タイトルスライドを追加", value=True)
    
    with col2:
        add_ending = st.checkbox("エンディングスライドを追加", value=True)
        
        # BGM選択
        bgm_files = [f for f in os.listdir('audio') if f.endswith('.mp3')] if os.path.exists('audio') else []
        bgm_options = ["なし"] + bgm_files
        selected_bgm = st.selectbox("BGM", options=bgm_options)
        bgm_path = os.path.join('audio', selected_bgm) if selected_bgm != "なし" else None
    
    # 動画生成ボタン
    if st.button("動画を生成"):
        with st.spinner("動画を生成中..."):
            # 動画生成オプションを設定
            video_generator.scene_duration = scene_duration
            video_generator.add_title = add_title
            video_generator.add_ending = add_ending
            
            # 動画を生成
            output_filename = f"tiktok_video_{int(time.time())}.mp4"
            output_path = video_generator.generate_video(
                st.session_state.scenes,
                st.session_state.media_dict,
                output_filename=output_filename,
                bgm_path=bgm_path
            )
            
            if output_path and os.path.exists(output_path):
                st.session_state.generated_video = output_path
                st.session_state.current_step = 4
                st.experimental_rerun()
            else:
                st.error("動画の生成に失敗しました。")
    
    # 前のステップへ戻るボタン
    if st.button("前のステップへ戻る"):
        st.session_state.current_step = 2
        st.experimental_rerun()

# ステップ4: 動画出力
elif st.session_state.current_step == 4:
    st.header("動画出力")
    
    if st.session_state.generated_video and os.path.exists(st.session_state.generated_video):
        st.write("動画が生成されました！")
        
        # 動画を表示
        video_file = open(st.session_state.generated_video, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        
        # 動画のダウンロードボタン
        with open(st.session_state.generated_video, "rb") as file:
            st.download_button(
                label="動画をダウンロード",
                data=file,
                file_name=os.path.basename(st.session_state.generated_video),
                mime="video/mp4"
            )
        
        # 操作ボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("動画設定を変更"):
                st.session_state.current_step = 3
                st.experimental_rerun()
        
        with col2:
            if st.button("最初からやり直す"):
                # セッション状態をリセット
                st.session_state.scenes = {}
                st.session_state.current_step = 1
                st.session_state.media_dict = {}
                st.session_state.generated_video = None
                st.experimental_rerun()
    else:
        st.error("動画ファイルが見つかりません。")
        if st.button("動画生成に戻る"):
            st.session_state.current_step = 3
            st.experimental_rerun()

# フッター
st.markdown("---")
st.markdown("© 2025 TikTok動画生成ツール")

import os
import requests
from dotenv import load_dotenv
import pixabay_python as pxb

# 環境変数の読み込み
load_dotenv()

class VideoSearch:
    def __init__(self):
        # APIキーの取得
        self.pixabay_api_key = os.getenv('PIXABAY_API_KEY', '')
        
        # APIクライアントの初期化
        self.init_api_clients()
    
    def init_api_clients(self):
        """APIクライアントを初期化する"""
        # Pixabay
        if self.pixabay_api_key:
            self.pixabay_client = pxb.PixabayClient(apiKey=self.pixabay_api_key)
        else:
            self.pixabay_client = None
    
    def search_pixabay_videos(self, keyword, per_page=3):
        """Pixabayから動画を検索する"""
        if not self.pixabay_client:
            return []
        
        try:
            # 日本語キーワードの場合はエンコードする
            encoded_keyword = requests.utils.quote(keyword)
            # Pixabayで動画検索
            search_result = self.pixabay_client.searchVideo(
                q=encoded_keyword,
                lang='ja',
                video_type='all',
                orientation='vertical',  # TikTok向けに縦長動画
                per_page=per_page
            )
            
            results = []
            if hasattr(search_result, 'hits'):
                hits_list = list(search_result.hits)
                for hit in hits_list:
                    results.append({
                        'id': hit.id,
                        'preview_url': hit.videos.tiny.url,
                        'medium_url': hit.videos.medium.url,
                        'large_url': hit.videos.large.url,
                        'source': 'Pixabay',
                        'source_url': hit.pageURL,
                        'width': hit.videos.medium.width,
                        'height': hit.videos.medium.height,
                        'tags': hit.tags,
                        'duration': hit.duration,
                        'type': 'video'
                    })
            return results
        except Exception as e:
            print(f"Pixabay動画検索エラー: {e}")
            return []
    
    def search_videos(self, keyword, per_page=3):
        """すべてのAPIから動画を検索する"""
        results = []
        
        # Pixabayから検索
        pixabay_results = self.search_pixabay_videos(keyword, per_page)
        results.extend(pixabay_results)
        
        # 将来的に他のAPIからの検索も追加可能
        
        return results
    
    def download_video(self, url, save_path):
        """動画をダウンロードする"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            return save_path
        except Exception as e:
            print(f"動画ダウンロードエラー: {e}")
            return None

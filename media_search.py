import os
import requests
import json
import time
import random
from dotenv import load_dotenv
import pixabay_python as pxb

# .envファイルから環境変数を読み込む
load_dotenv()

class MediaSearch:
    def __init__(self):
        """メディア検索クラスの初期化"""
        # APIキーの取得
        self.pixabay_api_key = os.getenv('PIXABAY_API_KEY', '')
        self.pexels_api_key = os.getenv('PEXELS_API_KEY', '')
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', '')
        
        # 検索サービスの設定
        self.search_services = ['pixabay', 'pexels', 'unsplash']
        
    def search_images(self, keyword, max_results=10):
        """キーワードに基づいて画像を検索する"""
        results = []
        
        # 検索サービスをランダムに選択
        random.shuffle(self.search_services)
        
        # 各サービスで検索
        for service in self.search_services:
            if len(results) >= max_results:
                break
                
            if service == 'pixabay' and self.pixabay_api_key:
                # Pixabayで検索
                pixabay_results = self._search_pixabay(keyword, max_results)
                results.extend(pixabay_results)
            
            elif service == 'pexels' and self.pexels_api_key:
                # Pexelsで検索
                pexels_results = self._search_pexels(keyword, max_results)
                results.extend(pexels_results)
            
            elif service == 'unsplash' and self.unsplash_access_key:
                # Unsplashで検索
                unsplash_results = self._search_unsplash(keyword, max_results)
                results.extend(unsplash_results)
        
        # 結果が最大数を超える場合はカット
        if len(results) > max_results:
            results = results[:max_results]
            
        return results
    
    def _search_pixabay(self, keyword, max_results=10):
        """Pixabay APIを使用して画像を検索する"""
        results = []
        
        try:
            # Pixabay APIクライアントの初期化
            pixabay_api = pxb.Pixabay(self.pixabay_api_key)
            
            # 画像検索
            response = pixabay_api.image_search(
                q=keyword,
                lang='ja',
                image_type='photo',
                orientation='vertical',  # TikTok向けに縦長画像
                per_page=max_results
            )
            
            # 結果の処理
            if 'hits' in response:
                for hit in response['hits']:
                    result = {
                        'id': hit['id'],
                        'title': hit.get('tags', '').split(',')[0],
                        'url': hit['largeImageURL'],
                        'thumbnail_url': hit['webformatURL'],
                        'source': 'pixabay',
                        'source_url': hit['pageURL']
                    }
                    results.append(result)
        except Exception as e:
            print(f"Pixabay検索エラー: {e}")
        
        return results
    
    def _search_pexels(self, keyword, max_results=10):
        """Pexels APIを使用して画像を検索する"""
        results = []
        
        try:
            # Pexels API URLの設定
            url = f"https://api.pexels.com/v1/search?query={keyword}&per_page={max_results}&orientation=portrait"
            
            # ヘッダーの設定
            headers = {
                'Authorization': self.pexels_api_key
            }
            
            # リクエストの送信
            response = requests.get(url, headers=headers) 
            data = response.json()
            
            # 結果の処理
            if 'photos' in data:
                for photo in data['photos']:
                    result = {
                        'id': photo['id'],
                        'title': photo.get('alt', ''),
                        'url': photo['src']['large'],
                        'thumbnail_url': photo['src']['medium'],
                        'source': 'pexels',
                        'source_url': photo['url']
                    }
                    results.append(result)
        except Exception as e:
            print(f"Pexels検索エラー: {e}")
        
        return results
    
    def _search_unsplash(self, keyword, max_results=10):
        """Unsplash APIを使用して画像を検索する"""
        results = []
        
        try:
            # Unsplash API URLの設定
            url = f"https://api.unsplash.com/search/photos?query={keyword}&per_page={max_results}&orientation=portrait"
            
            # ヘッダーの設定
            headers = {
                'Authorization': f"Client-ID {self.unsplash_access_key}"
            }
            
            # リクエストの送信
            response = requests.get(url, headers=headers) 
            data = response.json()
            
            # 結果の処理
            if 'results' in data:
                for photo in data['results']:
                    result = {
                        'id': photo['id'],
                        'title': photo.get('description', '') or photo.get('alt_description', ''),
                        'url': photo['urls']['regular'],
                        'thumbnail_url': photo['urls']['small'],
                        'source': 'unsplash',
                        'source_url': photo['links']['html']
                    }
                    results.append(result)
        except Exception as e:
            print(f"Unsplash検索エラー: {e}")
        
        return results
    
    def download_media(self, url, filename):
        """URLから画像をダウンロードして保存する"""
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                return filename
        except Exception as e:
            print(f"メディアダウンロードエラー: {e}")
        
        return None

import os
import random

class HashtagGenerator:
    def __init__(self):
        """ハッシュタグ生成クラスの初期化"""
        # カテゴリー別ハッシュタグ辞書
        self.hashtag_dict = {
            '料理': ['#レシピ', '#簡単料理', '#時短料理', '#おうちごはん', '#クッキング', 
                   '#料理好きな人と繋がりたい', '#おいしい', '#手料理', '#ヘルシー', 
                   '#おうちカフェ', '#おうち時間', '#料理初心者', '#料理動画', '#食べ物'],
            
            '旅行': ['#旅行', '#旅', '#絶景', '#観光', '#国内旅行', '#海外旅行', 
                   '#旅行好きな人と繋がりたい', '#trip', '#travel', '#景色', 
                   '#旅行記録', '#旅行好き', '#旅人', '#旅行女子', '#旅行男子'],
            
            'ファッション': ['#ファッション', '#コーデ', '#今日のコーデ', '#コーディネート', 
                       '#fashion', '#おしゃれ', '#おしゃれさんと繋がりたい', '#プチプラ', 
                       '#着回し', '#シンプルコーデ', '#大人コーデ', '#カジュアル', '#トレンド'],
            
            'ビューティー': ['#メイク', '#コスメ', '#スキンケア', '#美容', '#ヘアスタイル', 
                       '#ヘアアレンジ', '#ネイル', '#ナチュラルメイク', '#プチプラコスメ', 
                       '#ヘアカラー', '#ヘアケア', '#美容好きな人と繋がりたい', '#スキンケア好き'],
            
            'エンタメ': ['#エンタメ', '#映画', '#ドラマ', '#アニメ', '#音楽', '#漫画', 
                     '#ゲーム', '#映画好きな人と繋がりたい', '#アニメ好きな人と繋がりたい', 
                     '#ゲーム実況', '#推し', '#声優', '#歌ってみた', '#弾いてみた'],
            
            'スポーツ': ['#スポーツ', '#トレーニング', '#筋トレ', '#ワークアウト', '#ヨガ', 
                      '#ランニング', '#フィットネス', '#ダイエット', '#健康', '#ジム', 
                      '#スポーツ女子', '#スポーツ男子', '#運動', '#体幹トレーニング'],
            
            'ライフスタイル': ['#暮らし', '#日常', '#シンプルライフ', '#丁寧な暮らし', '#ミニマリスト', 
                        '#インテリア', '#収納', '#整理整頓', '#断捨離', '#持たない暮らし', 
                        '#シンプルな暮らし', '#ていねいな暮らし', '#日々の暮らし'],
            
            'ビジネス': ['#ビジネス', '#起業', '#副業', '#フリーランス', '#在宅ワーク', 
                      '#リモートワーク', '#投資', '#マーケティング', '#キャリア', '#転職', 
                      '#働き方', '#ビジネスマン', '#ビジネスウーマン', '#稼ぐ'],
            
            '教育': ['#勉強', '#学習', '#勉強法', '#受験', '#資格', '#英語', '#プログラミング', 
                   '#勉強垢', '#勉強記録', '#スタディ', '#study', '#参考書', '#大学受験', 
                   '#高校受験', '#資格勉強'],
            
            '一般': ['#TikTok', '#ティックトック', '#バズれ', '#バズり動画', '#おすすめ', 
                   '#おすすめにのりたい', '#いいね返し', '#フォロー返します', '#フォロバ100', 
                   '#拡散希望', '#拡散希望RT', '#動画', '#初投稿', '#トレンド']
        }
        
        # 人気のハッシュタグ（カテゴリーに関係なく使える）
        self.popular_hashtags = [
            '#TikTok', '#ティックトック', '#バズれ', '#おすすめ', '#おすすめにのりたい',
            '#いいね返し', '#フォロー返します', '#トレンド', '#初心者', '#初投稿',
            '#フォロバ', '#拡散希望', '#動画', '#viral', '#trend'
        ]
    
    def generate_hashtags(self, text, categories=None, max_tags=15):
        """テキストからハッシュタグを生成する"""
        # カテゴリーが指定されていない場合は、テキストから推測
        if not categories:
            categories = self._detect_categories(text)
        
        # 選択されたカテゴリーからハッシュタグを収集
        selected_hashtags = []
        for category in categories:
            if category in self.hashtag_dict:
                # カテゴリーごとに3〜5個のハッシュタグをランダムに選択
                num_tags = min(random.randint(3, 5), len(self.hashtag_dict[category]))
                category_tags = random.sample(self.hashtag_dict[category], num_tags)
                selected_hashtags.extend(category_tags)
        
        # 人気のハッシュタグから2〜3個をランダムに追加
        num_popular = min(random.randint(2, 3), len(self.popular_hashtags))
        popular_tags = random.sample(self.popular_hashtags, num_popular)
        selected_hashtags.extend(popular_tags)
        
        # 重複を削除し、最大数に制限
        unique_hashtags = list(set(selected_hashtags))
        if len(unique_hashtags) > max_tags:
            unique_hashtags = random.sample(unique_hashtags, max_tags)
        
        return unique_hashtags
    
    def _detect_categories(self, text):
        """テキストからカテゴリーを推測する"""
        # 各カテゴリーのキーワード
        category_keywords = {
            '料理': ['料理', 'レシピ', '食べ物', '調理', '美味しい', 'おいしい', '食材', '食事', 'クッキング', '味'],
            '旅行': ['旅行', '観光', '旅', '景色', '絶景', '名所', '観光地', '海外', '国内', 'ツアー', '旅程'],
            'ファッション': ['ファッション', '服', 'コーデ', 'スタイル', 'ブランド', 'アパレル', '着こなし', 'トレンド'],
            'ビューティー': ['メイク', '化粧', 'コスメ', '美容', 'スキンケア', 'ヘアスタイル', 'ネイル', '肌'],
            'エンタメ': ['映画', 'ドラマ', 'アニメ', '音楽', '漫画', 'ゲーム', 'エンタメ', '芸能', '俳優', '歌手'],
            'スポーツ': ['スポーツ', '運動', 'トレーニング', '筋トレ', 'ワークアウト', 'ヨガ', 'ランニング', '健康'],
            'ライフスタイル': ['暮らし', '生活', '日常', 'インテリア', '収納', '整理', '断捨離', 'シンプル'],
            'ビジネス': ['ビジネス', '仕事', '起業', '副業', 'フリーランス', '在宅', 'リモート', '投資', '稼ぐ'],
            '教育': ['勉強', '学習', '教育', '受験', '資格', '英語', 'プログラミング', '学校', '大学', '高校']
        }
        
        # テキストに含まれるキーワードからカテゴリーをスコアリング
        category_scores = {category: 0 for category in self.hashtag_dict.keys()}
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    category_scores[category] += 1
        
        # スコアが高い順にカテゴリーをソート
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        # スコアが1以上のカテゴリーを選択（最大3カテゴリー）
        detected_categories = [category for category, score in sorted_categories if score > 0][:3]
        
        # 検出されたカテゴリーがない場合は「一般」を追加
        if not detected_categories:
            detected_categories = ['一般']
        
        return detected_categories
    
    def format_hashtags(self, hashtags, separator=' '):
        """ハッシュタグをフォーマットする"""
        return separator.join(hashtags)

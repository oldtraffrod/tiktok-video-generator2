import os
from gtts import gTTS
import tempfile

class TextToSpeech:
    def __init__(self, output_dir="audio"):
        """音声合成クラスの初期化"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # デフォルト設定
        self.language = 'ja'
        self.slow = False
    
    def generate_speech(self, text, filename=None, language=None, slow=None):
        """テキストから音声を生成する"""
        try:
            # パラメータ設定
            lang = language if language else self.language
            speech_slow = slow if slow is not None else self.slow
            
            # ファイル名が指定されていない場合は一時ファイル名を生成
            if not filename:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir=self.output_dir)
                filename = os.path.basename(temp_file.name)
                temp_file.close()
            
            # 出力パスの設定
            if not filename.endswith('.mp3'):
                filename += '.mp3'
            output_path = os.path.join(self.output_dir, filename)
            
            # 音声合成
            tts = gTTS(text=text, lang=lang, slow=speech_slow)
            tts.save(output_path)
            
            return output_path
        except Exception as e:
            print(f"音声合成エラー: {e}")
            return None
    
    def generate_scene_audio(self, scenes, prefix="scene"):
        """シーンごとに音声を生成する"""
        audio_paths = {}
        
        for scene_id, scene_data in scenes.items():
            scene_text = scene_data['text']
            filename = f"{prefix}_{scene_id}.mp3"
            
            # 音声生成
            audio_path = self.generate_speech(scene_text, filename)
            if audio_path:
                audio_paths[scene_id] = audio_path
        
        return audio_paths
    
    def get_available_languages(self):
        """利用可能な言語のリストを返す"""
        # gTTSでサポートされている主要言語
        languages = {
            'ja': '日本語',
            'en': '英語',
            'zh-CN': '中国語（簡体）',
            'zh-TW': '中国語（繁体）',
            'ko': '韓国語',
            'fr': 'フランス語',
            'de': 'ドイツ語',
            'es': 'スペイン語',
            'it': 'イタリア語',
            'ru': 'ロシア語'
        }
        return languages

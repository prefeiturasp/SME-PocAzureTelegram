import unittest
from unittest.mock import patch
import src.main as main  # Ajuste conforme o caminho do seu módulo

class TestEnviarTelegram(unittest.TestCase):
    @patch('src.main.requests.post')
    def test_enviar_telegram(self, mock_post):
        msg = "Mensagem de teste"
        main.enviar_telegram(msg)

        expected_url = f"https://api.telegram.org/bot{main.TELEGRAM_TOKEN}/sendMessage"
        expected_payload = {
            "chat_id": main.TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }

        mock_post.assert_called_once_with(expected_url, json=expected_payload)

if __name__ == '__main__':
    unittest.main()

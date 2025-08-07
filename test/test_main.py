import unittest
from unittest.mock import patch, MagicMock
import src.main as main
from datetime import datetime, timedelta

class TestMain(unittest.TestCase):

    @patch('src.main.buscar_work_items')
    @patch('src.main.enviar_telegram')
    @patch('src.main.buscar_detalhes')
    def test_verificar_enviar_mensagem(self, mock_buscar_detalhes, mock_enviar_telegram, mock_buscar_work_items):
        # Mock dados
        mock_buscar_work_items.return_value = [1, 2]
        mock_buscar_detalhes.side_effect = [
            {"id":1, "fields": {"System.Title": "Teste 1", "System.State": "Novo", "System.WorkItemType": "Bug"}},
            {"id":2, "fields": {"System.Title": "Teste 2", "System.State": "Concluído", "System.WorkItemType": "PBI"}}
        ]
        mock_enviar_telegram.return_value = True

        # Limpa arquivo last_ids.json para teste isolado
        main.salvar_ids([])

        main.verificar()

        mock_buscar_work_items.assert_called_once()
        self.assertEqual(mock_buscar_detalhes.call_count, 2)
        self.assertEqual(mock_enviar_telegram.call_count, 2)

    @patch("src.main.requests.get")
    def test_requisicao_falha(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.text = "Erro interno"
        mock_get.return_value = mock_response

        result = main.buscar_work_items()
        self.assertNotEqual(result, {})

    @patch("src.main.enviar_telegram")
    def test_processar_work_items_vazio(self, mock_telegram):
        dados = {"value": []}
        main.buscar_work_items()
        mock_telegram.assert_not_called()

    @patch('src.main.requests.get')
    def test_buscar_detalhes_sucesso(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": 123, "title": "Teste"}
        mock_get.return_value = mock_response

        item_id = 123
        resultado = main.buscar_detalhes(item_id)

        expected_url = (
            f"{main.AZURE_ORG}/{main.AZURE_PROJECT}/_apis/wit/workitems/{item_id}?api-version=7.0"
        )
        mock_get.assert_called_once_with(expected_url, headers=main.headers)
        mock_response.raise_for_status.assert_called_once()
        self.assertEqual(resultado, {"id": 123, "title": "Teste"})

if __name__ == '__main__':
    unittest.main()

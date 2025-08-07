import unittest
from unittest.mock import mock_open, patch
import json

from src.main import carregar_ids, salvar_ids

class TestPersistenciaIds(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data='[1, 2, 3]')
    def test_carregar_ids_sucesso(self, mock_file):
        resultado = carregar_ids()
        self.assertEqual(resultado, [1, 2, 3])
        mock_file.assert_called_once_with('last_ids.json', 'r')  # STATE_FILE

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_carregar_ids_arquivo_nao_encontrado(self, mock_file):
        resultado = carregar_ids()
        self.assertEqual(resultado, [])  # Deve retornar lista vazia

    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_ids(self, mock_file):
        ids_para_salvar = [4, 5, 6]
        with patch("json.dump") as mock_dump:
            salvar_ids(ids_para_salvar)
            mock_file.assert_called_once_with('last_ids.json', 'w')  # STATE_FILE
            mock_dump.assert_called_once_with(ids_para_salvar, mock_file())
import unittest
from unittest.mock import patch, MagicMock
import importlib.metadata
from graphviz import Digraph
from your_module import get_dependencies, \
    create_dependency_graph  # Замените your_module на имя вашего файла, где находится код


class TestDependencyGraph(unittest.TestCase):

    @patch('importlib.metadata.distribution')
    def test_get_dependencies_success(self, mock_distribution):
        # Установим значения для тестирования успешного получения зависимостей
        mock_distribution.return_value.requires = ['numpy', 'pandas']
        result = get_dependencies('requests')
        self.assertEqual(result, ['numpy', 'pandas'])

    @patch('importlib.metadata.distribution')
    def test_get_dependencies_empty(self, mock_distribution):
        # Установим значения для тестирования случая, когда зависимостей нет
        mock_distribution.return_value.requires = None
        result = get_dependencies('requests')
        self.assertEqual(result, [])

    @patch('importlib.metadata.distribution')
    def test_get_dependencies_package_not_found(self, mock_distribution):
        # Симулируем, что пакет не найден
        mock_distribution.side_effect = importlib.metadata.PackageNotFoundError
        result = get_dependencies('unknown_package')
        self.assertEqual(result, [])

    @patch('importlib.metadata.distribution')
    def test_get_dependencies_other_exception(self, mock_distribution):
        # Симулируем другую ошибку
        mock_distribution.side_effect = Exception("Some error")
        with self.assertLogs(level='INFO') as log:
            result = get_dependencies('requests')
            self.assertEqual(result, [])
            self.assertIn("An error occurred: Some error", log.output[0])

    @patch('graphviz.Digraph')
    @patch('your_module.get_dependencies')  # Замените your_module на имя вашего файла с кодом
    def test_create_dependency_graph(self, mock_get_dependencies, mock_Digraph):
        mock_get_dependencies.return_value = ['numpy', 'pandas']
        mock_graph = MagicMock()
        mock_Digraph.return_value = mock_graph

        graph = create_dependency_graph('requests')
        mock_get_dependencies.assert_called_once_with('requests')
        self.assertEqual(graph.node.call_count, 3)  # 1 для requests + 2 для numpy и pandas
        self.assertEqual(graph.edge.call_count, 2)  # 2 ребра между requests и зависимостями


if __name__ == '__main__':
    unittest.main()
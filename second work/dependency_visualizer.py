import importlib.metadata
from graphviz import Digraph

def get_dependencies(package_name):
    try:
        # Получаем информацию о пакете
        distribution = importlib.metadata.distribution(package_name)
        dependencies = distribution.requires
        return [str(dep) for dep in dependencies] if dependencies else []
    except importlib.metadata.PackageNotFoundError:
        print(f"Package '{package_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def create_dependency_graph(package_name):
    dependencies = get_dependencies(package_name)

    # Создаем граф с помощью Graphviz
    graph = Digraph('G')

    graph.node(package_name)  # Основной пакет

    for dep in dependencies:
        graph.node(dep)  # Добавляем зависимость
        graph.edge(package_name, dep)  # Создаем связь

    return graph

# Пример использования
package_name = 'requests'  # Замените на нужный пакет
dependency_graph = create_dependency_graph(package_name)

# Сохранение графа в файл и отображение
dependency_graph.render('dependency_graph', format='png', cleanup=True)
dependency_graph.view()  # Показывает изображение графа
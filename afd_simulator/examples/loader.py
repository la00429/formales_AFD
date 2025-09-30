"""
Cargador de ejemplos para el Simulador de AFD.

Este módulo proporciona funcionalidad para cargar definiciones de AFD de ejemplo
desde archivos y gestionar colecciones de ejemplos.
"""

import os
from typing import List, Optional
from ..core.afd import AFD


class ExampleLoader:
    """
    Maneja la carga y gestión de definiciones de AFD de ejemplo.
    """
    
    def __init__(self, examples_directory: str = "afd_simulator/data"):
        """
        Inicializa el cargador de ejemplos.
        
        Args:
            examples_directory: Directorio que contiene los archivos de ejemplo
        """
        self.examples_directory = examples_directory
    
    def get_available_examples(self) -> List[str]:
        """
        Obtiene una lista de archivos de ejemplo disponibles.
        
        Returns:
            Lista de nombres de archivos de ejemplo (sin extensión)
        """
        if not os.path.exists(self.examples_directory):
            return []
        
        examples = []
        for filename in os.listdir(self.examples_directory):
            if filename.endswith('.json'):
                examples.append(filename[:-5])  # Elimina la extensión .json
        
        return sorted(examples)
    
    def load_example(self, example_name: str) -> AFD:
        """
        Carga un AFD de ejemplo desde un archivo.
        
        Args:
            example_name: Nombre del ejemplo a cargar
            
        Returns:
            Instancia de AFD cargada desde el archivo de ejemplo
            
        Raises:
            FileNotFoundError: Si el archivo de ejemplo no se encuentra
            Exception: Si hay un error al cargar el archivo
        """
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        
        if not os.path.exists(filename):
            available = self.get_available_examples()
            raise FileNotFoundError(f"Ejemplo '{example_name}' no encontrado. Ejemplos disponibles: {available}")
        
        return AFD.load_from_file(filename)
    
    def save_example(self, afd: AFD, example_name: str) -> None:
        """
        Guarda un AFD como ejemplo.
        
        Args:
            afd: El AFD a guardar
            example_name: Nombre para el archivo de ejemplo
        """
        if not os.path.exists(self.examples_directory):
            os.makedirs(self.examples_directory)
        
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        afd.save_to_file(filename)
    
    def get_example_info(self, example_name: str) -> dict:
        """
        Obtiene información sobre un AFD de ejemplo sin cargarlo completamente.
        
        Args:
            example_name: Nombre del ejemplo
            
        Returns:
            Diccionario con información del ejemplo
            
        Raises:
            FileNotFoundError: Si el archivo de ejemplo no se encuentra
        """
        filename = os.path.join(self.examples_directory, f"{example_name}.json")
        
        if not os.path.exists(filename):
            available = self.get_available_examples()
            raise FileNotFoundError(f"Ejemplo '{example_name}' no encontrado. Ejemplos disponibles: {available}")
        
        # Carga y retorna información resumida
        afd = AFD.load_from_file(filename)
        
        return {
            "name": example_name,
            "states": len(afd.states),
            "alphabet_size": len(afd.alphabet),
            "transitions": len(afd.transitions),
            "accepting_states": len(afd.accepting_states),
            "valid": afd.is_valid()
        }
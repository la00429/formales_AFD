"""
Implementación de Autómata Finito Determinista (AFD)

Este módulo contiene la clase AFD que representa un autómata finito determinista
con los cinco componentes requeridos: estados (Q), alfabeto (Σ), estado inicial (q₀),
estados de aceptación (F) y función de transición (δ).
"""

import json
from typing import Set, Dict, List, Tuple, Optional


class AFD:
    """
    Representa un Autómata Finito Determinista (AFD).
    
    Un AFD se define mediante la 5-tupla (Q, Σ, δ, q₀, F) donde:
    - Q: Conjunto finito de estados
    - Σ: Alfabeto (conjunto de símbolos de entrada)
    - δ: Función de transición Q × Σ → Q
    - q₀: Estado inicial
    - F: Conjunto de estados de aceptación
    """
    
    def __init__(self):
        """Inicializa un AFD vacío."""
        self.states: Set[str] = set()
        self.alphabet: Set[str] = set()
        self.initial_state: Optional[str] = None
        self.accepting_states: Set[str] = set()
        self.transitions: Dict[Tuple[str, str], str] = {}
    
    def add_state(self, state: str) -> None:
        """
        Agrega un estado al AFD.
        
        Args:
            state: El identificador del estado a agregar
        """
        self.states.add(state)
    
    def add_symbol(self, symbol: str) -> None:
        """
        Agrega un símbolo al alfabeto.
        
        Args:
            symbol: El símbolo a agregar al alfabeto
        """
        self.alphabet.add(symbol)
    
    def set_initial_state(self, state: str) -> None:
        """
        Establece el estado inicial del AFD.
        
        Args:
            state: El identificador del estado inicial
            
        Raises:
            ValueError: Si el estado no está en el conjunto de estados
        """
        if state not in self.states:
            raise ValueError(f"El estado '{state}' no está en el conjunto de estados")
        self.initial_state = state
    
    def add_accepting_state(self, state: str) -> None:
        """
        Agrega un estado al conjunto de estados de aceptación.
        
        Args:
            state: El identificador del estado de aceptación
            
        Raises:
            ValueError: Si el estado no está en el conjunto de estados
        """
        if state not in self.states:
            raise ValueError(f"El estado '{state}' no está en el conjunto de estados")
        self.accepting_states.add(state)
    
    def add_transition(self, from_state: str, symbol: str, to_state: str) -> None:
        """
        Agrega una transición a la función de transición.
        
        Args:
            from_state: Estado origen de la transición
            symbol: Símbolo de entrada que activa la transición
            to_state: Estado destino de la transición
            
        Raises:
            ValueError: Si alguno de los estados o el símbolo no están definidos
        """
        if from_state not in self.states:
            raise ValueError(f"El estado origen '{from_state}' no está en el conjunto de estados")
        if to_state not in self.states:
            raise ValueError(f"El estado destino '{to_state}' no está en el conjunto de estados")
        if symbol not in self.alphabet:
            raise ValueError(f"El símbolo '{symbol}' no está en el alfabeto")
        
        self.transitions[(from_state, symbol)] = to_state
    
    def is_valid(self) -> bool:
        """
        Verifica si el AFD está correctamente definido.
        
        Returns:
            True si el AFD es válido, False en caso contrario
        """
        # Verifica si todos los componentes requeridos están definidos
        if not self.states:
            return False
        if not self.alphabet:
            return False
        if self.initial_state is None:
            return False
        if self.initial_state not in self.states:
            return False
        if not self.accepting_states.issubset(self.states):
            return False
        
        # Verifica si todas las transiciones están definidas para cada par estado-símbolo
        for state in self.states:
            for symbol in self.alphabet:
                if (state, symbol) not in self.transitions:
                    return False
        
        return True
    
    def evaluate_string(self, input_string: str) -> Tuple[bool, List[Tuple[str, str, str]]]:
        """
        Evalúa si una cadena es aceptada por el AFD.
        
        Args:
            input_string: La cadena a evaluar
            
        Returns:
            Una tupla que contiene:
            - Booleano indicando si la cadena es aceptada
            - Lista de transiciones mostrando el camino recorrido
            
        Raises:
            ValueError: Si el AFD no es válido o contiene símbolos inválidos
        """
        if not self.is_valid():
            raise ValueError("El AFD no está correctamente definido")
        
        # Verifica si todos los símbolos de la cadena están en el alfabeto
        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"El símbolo '{symbol}' no está en el alfabeto")
        
        # Simula el AFD
        current_state = self.initial_state
        transitions_path = []
        
        for symbol in input_string:
            next_state = self.transitions.get((current_state, symbol))
            if next_state is None:
                raise ValueError(f"No hay transición definida para el estado '{current_state}' con el símbolo '{symbol}'")
            
            transitions_path.append((current_state, symbol, next_state))
            current_state = next_state
        
        # Verifica si el estado final es de aceptación
        is_accepted = current_state in self.accepting_states
        
        return is_accepted, transitions_path
    
    def generate_accepted_strings(self, max_count: int = 10) -> List[str]:
        """
        Genera las primeras n cadenas más cortas aceptadas por el AFD.
        
        Args:
            max_count: Número máximo de cadenas a generar
            
        Returns:
            Lista de cadenas aceptadas ordenadas por longitud
            
        Raises:
            ValueError: Si el AFD no es válido
        """
        if not self.is_valid():
            raise ValueError("El AFD no está correctamente definido")
        
        accepted_strings = []
        alphabet_list = list(self.alphabet)
        
        # Usa BFS para encontrar los caminos más cortos a los estados de aceptación
        queue = [("", self.initial_state)]
        visited = set()
        
        while queue and len(accepted_strings) < max_count:
            current_string, current_state = queue.pop(0)
            
            # Omite si ya hemos visitado este estado con esta longitud de cadena
            state_length_key = (current_state, len(current_string))
            if state_length_key in visited:
                continue
            visited.add(state_length_key)
            
            # Si el estado actual es de aceptación, agrega la cadena a los resultados
            if current_state in self.accepting_states and current_string:
                accepted_strings.append(current_string)
            
            # Agrega transiciones para cada símbolo
            for symbol in alphabet_list:
                next_state = self.transitions.get((current_state, symbol))
                if next_state is not None:
                    next_string = current_string + symbol
                    queue.append((next_string, next_state))
        
        return accepted_strings[:max_count]
    
    def save_to_file(self, filename: str) -> None:
        """
        Guarda la definición del AFD en un archivo JSON.
        
        Args:
            filename: Nombre del archivo donde guardar
        """
        # Convertir transiciones a formato más robusto
        transitions_list = []
        for (from_state, symbol), to_state in self.transitions.items():
            transitions_list.append({
                "from_state": from_state,
                "symbol": symbol,
                "to_state": to_state
            })
        
        afd_data = {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "initial_state": self.initial_state,
            "accepting_states": list(self.accepting_states),
            "transitions": transitions_list
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(afd_data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'AFD':
        """
        Carga la definición de un AFD desde un archivo JSON.
        
        Args:
            filename: Nombre del archivo a cargar
            
        Returns:
            Instancia de AFD cargada desde el archivo
        """
        with open(filename, 'r', encoding='utf-8') as f:
            afd_data = json.load(f)
        
        afd = cls()
        
        # Carga los estados
        for state in afd_data["states"]:
            afd.add_state(state)
        
        # Carga el alfabeto
        for symbol in afd_data["alphabet"]:
            afd.add_symbol(symbol)
        
        # Carga el estado inicial (solo si no es None)
        if afd_data["initial_state"] is not None:
            afd.set_initial_state(afd_data["initial_state"])
        
        # Carga los estados de aceptación
        for state in afd_data["accepting_states"]:
            afd.add_accepting_state(state)
        
        # Carga las transiciones
        transitions = afd_data["transitions"]
        
        # Manejar tanto el formato antiguo (dict con claves separadas por comas) 
        # como el nuevo formato (lista de objetos)
        if isinstance(transitions, list):
            # Nuevo formato: lista de objetos
            for transition in transitions:
                from_state = transition["from_state"]
                symbol = transition["symbol"]
                to_state = transition["to_state"]
                afd.add_transition(from_state, symbol, to_state)
        else:
            # Formato antiguo: diccionario con claves separadas por comas
            # Usar un separador más robusto para manejar comas en nombres
            # Buscar la última coma que separa el estado del símbolo
            for transition_key, to_state in transitions.items():
                last_comma_index = transition_key.rfind(',')
                if last_comma_index == -1:
                    raise ValueError(f"Formato de transición inválido: {transition_key}")
                
                from_state = transition_key[:last_comma_index]
                symbol = transition_key[last_comma_index + 1:]
                afd.add_transition(from_state, symbol, to_state)
        
        return afd
    
    def __str__(self) -> str:
        """Retorna una representación en cadena del AFD."""
        return f"""Definición del AFD:
Estados (Q): {sorted(self.states)}
Alfabeto (Σ): {sorted(self.alphabet)}
Estado Inicial (q₀): {self.initial_state}
Estados de Aceptación (F): {sorted(self.accepting_states)}
Transiciones (δ):
{chr(10).join(f"  δ({from_state}, {symbol}) = {to_state}" 
              for (from_state, symbol), to_state in sorted(self.transitions.items()))}
Válido: {self.is_valid()}"""

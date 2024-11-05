class TuringMachine:
    def __init__(self):
        # Definir los componentes de la máquina de Turing
        self.states = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}
        self.current_state = 'q0'
        self.final_states = {'q6'}
        self.tape1 = []
        self.tape2 = []
        self.head1 = 0
        self.head2 = 0
        self.direction = "right"  # Dirección de lectura inicial

        # Transiciones para la máquina de Turing
        self.transitions = {
            # Transiciones para el estado inicial q0
            ('q0', 'a', 'a'): ('q1', 'a', 'a', 'R', 'R'),
            ('q0', 'a', 'b'): ('q1', 'a', 'b', 'R', 'R'),
            ('q0', 'b', 'a'): ('q1', 'b', 'a', 'R', 'R'),
            ('q0', 'b', 'b'): ('q1', 'b', 'b', 'R', 'R'),
            ('q0', '#', '#'): ('q6', '#', '#', 'R', 'R'),  # Aceptación si ambos alcanzan '#'

            # Transiciones en el estado q1 (procesando caracteres)
            ('q1', 'a', 'a'): ('q1', 'a', 'a', 'R', 'R'),
            ('q1', 'a', 'b'): ('q2', 'a', 'b', 'L', 'L'),
            ('q1', 'b', 'a'): ('q2', 'b', 'a', 'L', 'L'),
            ('q1', 'b', 'b'): ('q1', 'b', 'b', 'R', 'R'),
            ('q1', '#', '#'): ('q6', '#', '#', 'R', 'R'),  # Aceptación si ambos alcanzan '#'

            # Transiciones para el estado q2 (retroceso)
            ('q2', 'a', 'a'): ('q3', 'a', 'a', 'L', 'L'),
            ('q2', 'b', 'b'): ('q3', 'b', 'b', 'L', 'L'),
            ('q2', '#', '#'): ('q6', '#', '#', 'R', 'R'),  # Aceptación si ambos alcanzan '#'

            # Transiciones en estado q3 (retroceso continuo)
            ('q3', 'a', 'a'): ('q3', 'a', 'a', 'L', 'L'),
            ('q3', 'b', 'b'): ('q3', 'b', 'b', 'L', 'L'),
            ('q3', '#', '#'): ('q0', '#', '#', 'R', 'R'),  # Reiniciar a q0 si ambos alcanzan '#'

            # Estado de aceptación
            ('q6', '#', '#'): ('q6', '#', '#', 'R', 'R'),  # Estado de aceptación final
        }
        self.transition_log = []  # Para almacenar las transiciones para el árbol de derivación y la tabla

    def reset(self):
        """Reinicia la máquina de Turing."""
        self.current_state = 'q0'
        self.head1 = 0
        self.head2 = 0
        self.transition_log.clear()
        self.direction = "right"

    def load_tapes(self, input_string):
        """Carga la cadena de entrada en las dos cintas."""
        self.tape1 = list(input_string)
        self.tape2 = list(input_string)
        self.head1 = 0
        self.head2 = 0

    def ensure_tape_length(self, tape, head_position):
        """Expande la cinta con '#' si el cabezal se mueve fuera de los límites."""
        while head_position >= len(tape):
            tape.append('#')
        while head_position < 0:
            tape.insert(0, '#')
            head_position += 1
        return head_position

    def transition(self):
        """Realiza una transición en la máquina de Turing."""
        # Asegurar que los cabezales estén dentro de los límites de las cintas
        self.head1 = self.ensure_tape_length(self.tape1, self.head1)
        self.head2 = self.ensure_tape_length(self.tape2, self.head2)

        # Leer símbolos actuales
        symbol1 = self.tape1[self.head1]
        symbol2 = self.tape2[self.head2]
        key = (self.current_state, symbol1, symbol2)

        if key in self.transitions:
            # Realizar transición
            new_state, write1, write2, move1, move2 = self.transitions[key]
            self.tape1[self.head1] = write1
            self.tape2[self.head2] = write2
            self.transition_log.append((self.current_state, symbol1, symbol2, new_state))  # Log the transition
            self.current_state = new_state
            self.head1 += 1 if move1 == 'R' else -1
            self.head2 += 1 if move2 == 'R' else -1
        else:
            self.current_state = None  # Transición inválida, detiene la máquina

    def process_string(self, input_string, direction="right"):
        """Procesa la cadena en la dirección indicada (izquierda o derecha)."""
        self.load_tapes(input_string)
        self.direction = direction
        if direction == "left":
            self.tape1.reverse()
            self.tape2.reverse()

        while self.current_state and self.current_state not in self.final_states:
            self.transition()
        return self.current_state in self.final_states

    def get_simbologia(self):
        """Muestra la simbología de la máquina de Turing."""
        return f"M = (Q={self.states}, Σ={{a, b, #, *}}, δ, q0, F={self.final_states})"

    def show_derivation_tree(self):
        """Muestra el árbol de derivación."""
        tree = []
        for step in self.transition_log:
            current_state, symbol1, symbol2, new_state = step
            tree.append(f"{current_state} --({symbol1}, {symbol2})--> {new_state}")
        return tree

    def show_transition_table(self):
        """Muestra la tabla de transición."""
        table = [["Estado Actual", "Símbolo Cinta 1", "Símbolo Cinta 2", "Nuevo Estado"]]
        for step in self.transition_log:
            current_state, symbol1, symbol2, new_state = step
            table.append([current_state, symbol1, symbol2, new_state])
        return table


# Lista de cadenas para procesar
input_strings = ["aba", "baa", "ab#", "aab*", "baab#", "abba#", "aaa#", "abab#", "bbaa*", "a#"]

# Crear instancia de la máquina de Turing
tm = TuringMachine()

# Procesar cada cadena en ambas direcciones y mostrar los resultados
for string in input_strings:
    for direction in ["right", "left"]:
        print(f"\nProcesando cadena: {string} en dirección {direction}")
        
        # Reiniciar y procesar la cadena
        tm.reset()
        is_valid = tm.process_string(string, direction)
        
        # Mostrar el árbol de derivación para esta cadena
        print("Árbol de derivación:")
        derivation_tree = tm.show_derivation_tree()
        if derivation_tree:
            for step in derivation_tree:
                print(step)
        else:
            print("No se encontraron transiciones válidas para esta cadena.")
        
        # Mostrar la tabla de transición para esta cadena
        print("Tabla de transición:")
        transition_table = tm.show_transition_table()
        for row in transition_table:
            print(row)
        
        # Mostrar simbología de la máquina
        print("Simbología de la máquina de Turing:")
        print(tm.get_simbologia())
        
        # Resultado final de la cadena
        print(f"Resultado: {'Cadena válida' if is_valid else 'Cadena inválida'}")



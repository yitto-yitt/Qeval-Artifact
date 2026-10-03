# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        for pauli_string, t in zip(pauli_strings, times):
            ops = []
            for wire, char in enumerate(pauli_string):
                if char == 'I':
                    continue
                elif char == 'X':
                    ops.append(qml.PauliX(wire))
                elif char == 'Y':
                    ops.append(qml.PauliY(wire))
                elif char == 'Z':
                    ops.append(qml.PauliZ(wire))
                else:
                    raise ValueError(f"Unknown Pauli character: {char}")
            if not ops:
                continue
            elif len(ops) == 1:
                ham = ops[0]
            else:
                ham = qml.prod(*ops)
            qml.exp(ham, -1j * t)
        return qml.state()
    return circuit

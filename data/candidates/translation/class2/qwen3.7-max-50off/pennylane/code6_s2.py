# EVAL_META: task_id=6, framework=pennylane, class=2
import pennylane as qml

def create_state_prep(num_qubits):
    state = [0] * (num_qubits - 1) + [1]
    ops = [qml.BasisState(state, wires=range(num_qubits))]
    return qml.tape.QuantumScript(ops)

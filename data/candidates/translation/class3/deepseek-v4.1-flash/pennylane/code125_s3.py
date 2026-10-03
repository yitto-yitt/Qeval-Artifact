# EVAL_META: task_id=125, framework=pennylane, class=3
import pennylane as qml

def circ_to_gate(circ):
    my_circuit = qml.from_qiskit(circ)
    matrix = qml.matrix(my_circuit)(wires=range(circ.num_qubits))
    return qml.QubitUnitary(matrix, wires=range(circ.num_qubits))

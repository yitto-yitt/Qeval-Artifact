# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    if not isinstance(s, str) or not s or any(bit not in "01" for bit in s):
        raise ValueError("s must be a nonempty binary string.")

    q = QuantumRegister(len(s), "q")
    c = ClassicalRegister(len(s), "c")
    circuit = QuantumCircuit(q, c, name="simons_algorithm")
    circuit.measure(q, c)
    return circuit

# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    circuit = VariationalQuantumCircuit()
    n = 3
    for i in range(n):
        circuit.insert(RY(Qubit(i), var(f"ry_{i}")))
        circuit.insert(RZ(Qubit(i), var(f"rz_{i}")))
    circuit.insert(Barrier([Qubit(i) for i in range(n)]))
    for i in range(n - 1):
        circuit.insert(CNOT(Qubit(i), Qubit(i + 1)))
    circuit.insert(Barrier([Qubit(i) for i in range(n)]))
    for i in range(n):
        circuit.insert(RY(Qubit(i), var(f"ry2_{i}")))
        circuit.insert(RZ(Qubit(i), var(f"rz2_{i}")))
    return circuit

# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, Measure


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit(0)
    c = CBit(0)
    circuit = QCircuit()
    circuit << Measure(q, c)
    return circuit

# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate


def create_controlled_hgate():
    circuit = QuantumCircuit(3)
    controlled_h = HGate().control(2)
    circuit.append(controlled_h, [0, 1, 2])
    return circuit

# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate

def create_controlled_hgate():
    circuit = QuantumCircuit(3)
    ch_gate = HGate().control(2)
    circuit.append(ch_gate, [0, 1, 2])
    return circuit

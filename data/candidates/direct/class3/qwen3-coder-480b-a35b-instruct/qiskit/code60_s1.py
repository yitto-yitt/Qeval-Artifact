# EVAL_META: task_id=60, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import SGate, SdgGate
from qiskit.quantum_info import Operator

def create_cy_gate():
    qc = QuantumCircuit(2)
    qc.sdg(1)
    qc.cx(0, 1)
    qc.s(1)
    return qc.to_gate(label='CY')

# EVAL_META: task_id=81, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.qasm2 import dumps, loads

def convert_qasm_string_to_quantum_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qasm_str = dumps(qc)
    return loads(qasm_str)

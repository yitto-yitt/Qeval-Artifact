# EVAL_META: task_id=27, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.circuit.library import HGate, CXGate


def apply_op_back():
    qc = QuantumCircuit(3)
    qc.append(HGate(), [0])
    qc.append(CXGate(), [0, 1])

    dag = circuit_to_dag(qc)
    dag.apply_operation_back(HGate(), [dag.qubits[0]], [])

    return dag

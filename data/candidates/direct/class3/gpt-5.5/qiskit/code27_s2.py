# EVAL_META: task_id=27, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.circuit.library.standard_gates import HGate


def apply_op_back():
    circuit = QuantumCircuit(3)
    circuit.h(0)
    circuit.cx(0, 1)

    dag = circuit_to_dag(circuit)
    dag.apply_operation_back(HGate(), qargs=[dag.qubits[0]], cargs=[])

    return dag

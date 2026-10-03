# EVAL_META: task_id=27, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.circuit.library import HGate

def apply_op_back():
    # Create a 3-qubit Quantum Circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    
    # Convert the circuit to DAG
    dag = circuit_to_dag(qc)
    
    # Apply a Hadamard operation to the back of qubit 0
    dag.apply_operation_back(HGate(), qargs=[dag.qubits[0]])
    
    return dag

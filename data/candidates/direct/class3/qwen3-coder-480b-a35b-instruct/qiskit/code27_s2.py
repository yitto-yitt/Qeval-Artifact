# EVAL_META: task_id=27, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.library import HGate, CXGate


def apply_op_back():
    # Create initial quantum circuit
    qc = QuantumCircuit(3)
    qc.h(0)  # H gate on qubit 0
    qc.cx(0, 1)  # CX gate on qubit 0 and 1
    
    # Convert circuit to DAG
    dag = circuit_to_dag(qc)
    
    # Apply a Hadamard operation to the back of qubit 0
    h_gate = HGate()
    dag.apply_operation_back(h_gate, [dag.qubits[0]], [])
    
    return dag

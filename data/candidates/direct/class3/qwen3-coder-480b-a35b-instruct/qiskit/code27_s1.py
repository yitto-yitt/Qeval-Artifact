# EVAL_META: task_id=27, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.circuit.library import HGate

def apply_op_back():
    # Create the initial quantum circuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    
    # Convert to DAG
    dag = circuit_to_dag(qc)
    
    # Apply Hadamard gate to qubit 0 at the end
    h_gate = HGate()
    dag.apply_operation_back(h_gate, [0], [])
    
    return dag

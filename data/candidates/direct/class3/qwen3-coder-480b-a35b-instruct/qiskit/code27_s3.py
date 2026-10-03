# EVAL_META: task_id=27, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag, dag_to_circuit


def apply_op_back():
    # Create the initial quantum circuit
    qc = QuantumCircuit(3)
    qc.h(0)  # H gate on qubit 0
    qc.cx(0, 1)  # CX gate on qubit 0 and 1
    
    # Convert the circuit to DAG
    dag = circuit_to_dag(qc)
    
    # Apply a Hadamard operation to the back of qubit 0 in the DAG
    from qiskit.circuit.library import HGate
    h_gate = HGate()
    qubit_0 = dag.qubits[0]
    dag.apply_operation_back(h_gate, [qubit_0], [])
    
    return dag

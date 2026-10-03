# EVAL_META: task_id=26, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag

def bell_dag():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    
    dag = circuit_to_dag(qc)
    return dag

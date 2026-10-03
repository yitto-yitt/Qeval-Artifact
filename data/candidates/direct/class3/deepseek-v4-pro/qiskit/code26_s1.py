# EVAL_META: task_id=26, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.dagcircuit import DAGCircuit

def bell_dag():
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0, 1)
    dag = DAGCircuit.from_circuit(qc)
    return dag

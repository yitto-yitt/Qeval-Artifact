# EVAL_META: task_id=23, framework=qiskit, class=3
from qiskit import QuantumCircuit

def dj_constant_oracle():
    # Create a QuantumCircuit with 3 qubits (0 and 1 as inputs, 2 as output)
    oracle = QuantumCircuit(3)
    # Since it's a constant-one oracle, we always flip the state of the output qubit (qubit 2)
    oracle.x(2)
    return oracle

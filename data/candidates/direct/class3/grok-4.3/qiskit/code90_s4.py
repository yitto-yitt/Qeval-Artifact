# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    base = QuantumCircuit(2)
    base.x(0)
    base.h(1)
    custom = base.to_gate()
    controlled = custom.control(2)
    circuit = QuantumCircuit(4)
    circuit.append(controlled, [0, 3, 1, 2])
    return circuit

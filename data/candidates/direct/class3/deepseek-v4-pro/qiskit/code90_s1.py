# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    qc_custom = QuantumCircuit(2)
    qc_custom.x(0)          # X gate on qubit 0 (becomes target qubit 1 when controlled)
    qc_custom.h(1)          # H gate on qubit 1 (becomes target qubit 2 when controlled)
    custom_gate = qc_custom.to_gate(label='XH')
    
    controlled_gate = custom_gate.control(2)  # add two control qubits
    
    circuit = QuantumCircuit(4)
    circuit.append(controlled_gate, [0, 3, 1, 2])  # controls: 0,3; targets: 1,2
    return circuit

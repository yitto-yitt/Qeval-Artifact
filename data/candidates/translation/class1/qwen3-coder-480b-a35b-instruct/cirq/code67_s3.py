# EVAL_META: task_id=67, framework=cirq, class=1
import cirq
import numpy as np


def chsh_circuit(alice, bob):
    qubits = [cirq.LineQubit(i) for i in range(2)]
    circuit = cirq.Circuit()
    
    # Create entangled pair (Bell state)
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Barrier equivalent - just continue
    if alice == 0:
        # No rotation needed (equivalent to ry(0))
        pass
    else:
        circuit.append(cirq.ry(-np.pi / 2)(qubits[0]))
    
    # Measure Alice's qubit
    circuit.append(cirq.measure(qubits[0], key='alice_out'))
    
    if bob == 0:
        circuit.append(cirq.ry(-np.pi / 4)(qubits[1]))
    else:
        circuit.append(cirq.ry(np.pi / 4)(qubits[1]))
    
    # Measure Bob's qubit
    circuit.append(cirq.measure(qubits[1], key='bob_out'))
    
    return circuit

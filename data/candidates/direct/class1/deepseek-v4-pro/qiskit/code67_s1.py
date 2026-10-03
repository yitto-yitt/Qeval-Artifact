# EVAL_META: task_id=67, framework=qiskit, class=1
from qiskit import QuantumCircuit
from math import pi

def chsh_circuit(alice, bob):
    # Create a 2-qubit circuit (plus classical bits for measurement later)
    circuit = QuantumCircuit(2)
    # Prepare Bell state |Φ+⟩
    circuit.h(0)
    circuit.cx(0, 1)

    # Alice's measurement basis selection
    if alice == 0:
        # Measure in Z-basis: no rotation needed
        pass
    elif alice == 1:
        # Measure in X-basis: apply Hadamard to rotate X → Z
        circuit.h(0)
    else:
        raise ValueError("alice must be 0 or 1")

    # Bob's measurement basis selection
    if bob == 0:
        # Measure in (X+Z)/√2: rotate by +π/4 around Y
        circuit.ry(pi / 4, 1)
    elif bob == 1:
        # Measure in (X-Z)/√2: rotate by -π/4 around Y
        circuit.ry(-pi / 4, 1)
    else:
        raise ValueError("bob must be 0 or 1")

    # Measure all qubits (adds classical bits and measurement instructions)
    circuit.measure_all()
    return circuit

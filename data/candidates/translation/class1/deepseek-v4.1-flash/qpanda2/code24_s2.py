# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def dj_algorithm(oracle):
    # Extract qubits from the oracle circuit
    qubits = oracle.get_qubits()
    # Sort by physical index to ensure deterministic order (matches allocation order)
    qubits = sorted(qubits, key=lambda q: q.get_phy_qubit())
    n = len(qubits)
    if n < 2:
        raise ValueError("Oracle must have at least 2 qubits")

    # Get the QVM instance from the first qubit
    qvm = qubits[0].get_qvm()
    # Allocate classical bits for the input register (n-1 bits)
    cbits = qvm.cAlloc_many(n - 1)

    # Build the Deutsch-Jozsa circuit
    prog = QProg()
    # Apply X to the output qubit (last qubit)
    prog << X(qubits[-1])
    # Apply Hadamard to all qubits
    for q in qubits:
        prog << H(q)
    # Apply the oracle
    prog << oracle
    # Apply Hadamard to all qubits again
    for q in qubits:
        prog << H(q)
    # Measure the input qubits
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])

    # Run the quantum program
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)

    # Convert counts to probabilities
    total = builtins.sum(result.values())
    if total == 0:
        return {}
    return {key: value / total for key, value in result.items()}

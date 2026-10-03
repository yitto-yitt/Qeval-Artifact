# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit, OriginQubitPool, OriginCMem


def bv_algorithm(s):
    n = len(s)
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = [machine.qAlloc() for _ in range(n + 1)]
    cbits = [machine.cAlloc() for _ in range(n)]

    prog = QProg()

    # Initialize ancilla qubit to |1>
    prog << pq.X(qubits[n])

    # Apply Hadamard to all qubits
    for i in range(n + 1):
        prog << pq.H(qubits[i])

    # Apply controlled-X gates based on secret string s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CX(qubits[index], qubits[n])

    # Apply Hadamard to first n qubits
    for i in range(n):
        prog << pq.H(qubits[i])

    # Measure first n qubits
    for i in range(n):
        prog << pq.Measure(qubits[i], cbits[i])

    result = pq.run_with_configuration(prog, machine, 1)
    
    # Extract bitstrings from result
    bitstrings = []
    for key in result.keys():
        bitstring = key
        bitstrings.append(bitstring)

    pq.destroy_quantum_machine(machine)
    return [bitstrings, result]

# EVAL_META: task_id=37, framework=qpanda, class=1
import pyqpanda3.core as pq

def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    # allocate qubits and classical bits
    qubits = machine.qAlloc_many(n + 1)
    cbits = machine.cAlloc_many(n)
    # build quantum program
    prog = pq.QProg()
    ancilla = n  # index of the ancilla qubit
    # prepare ancilla in |1>
    prog.insert(pq.X(qubits[ancilla]))
    # apply Hadamard to all qubits
    for q in qubits:
        prog.insert(pq.H(q))
    # oracle: CNOT gates for bits of s
    for idx, bit in enumerate(reversed(s)):
        if bit == '1':
            prog.insert(pq.CNOT(qubits[idx], qubits[ancilla]))
    # final Hadamard on data qubits
    for i in range(n):
        prog.insert(pq.H(qubits[i]))
    # measurement
    for i in range(n):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    # execute
    result = machine.run_with_configuration(prog, cbits, shots=1)
    bitstrings = list(result.keys())
    machine.finalize()
    return [bitstrings, result]

# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(n + 1)
        cbits = machine.cAlloc_many(n)
        ancilla = qubits[n]
        program = pq.QProg()

        program << pq.X(ancilla)
        for qubit in qubits:
            program << pq.H(qubit)

        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                program << pq.CNOT(qubits[index], ancilla)

        for index in range(n):
            program << pq.H(qubits[index])

        for index in range(n):
            program << pq.Measure(qubits[index], cbits[index])

        result = machine.run_with_configuration(program, cbits, 1)
        bitstrings = [
            bitstring
            for bitstring, count in result.items()
            for _ in range(count)
        ]
        return [bitstrings, result]
    finally:
        machine.finalize()

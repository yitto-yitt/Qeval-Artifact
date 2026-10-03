# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        q = machine.qAlloc_many(n + 1)
        meas = machine.cAlloc_many(n)
        ancilla = q[n]
        program = pq.QProg()

        program << pq.X(ancilla)
        for qubit in q:
            program << pq.H(qubit)

        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                program << pq.CNOT(q[index], ancilla)

        for index in range(n):
            program << pq.H(q[index])
        for index in range(n):
            program << pq.Measure(q[index], meas[index])

        result = machine.run_with_configuration(program, meas, 1)
        bitstrings = [
            bitstring
            for bitstring, count in result.items()
            for _ in range(count)
        ]
        return [bitstrings, result]
    finally:
        machine.finalize()

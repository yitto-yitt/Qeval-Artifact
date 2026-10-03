# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    shots = 1

    c0_first = False
    if n > 1:
        cal_machine = pq.CPUQVM()
        cal_machine.init_qvm()
        cal_q = cal_machine.qAlloc_many(2)
        cal_c = cal_machine.cAlloc_many(2)
        cal_prog = pq.QProg()
        cal_prog << pq.X(cal_q[0])
        cal_prog << pq.Measure(cal_q[0], cal_c[0])
        cal_prog << pq.Measure(cal_q[1], cal_c[1])
        cal_counts = dict(cal_machine.run_with_configuration(cal_prog, cal_c, 1))
        cal_key = next(iter(cal_counts.keys()), "")
        c0_first = len(cal_key) >= 2 and cal_key[0] == "1" and cal_key[1] == "0"
        cal_machine.finalize()

    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    prog = pq.QProg()
    ancilla = n

    prog << pq.X(q[ancilla])
    for i in range(n + 1):
        prog << pq.H(q[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[ancilla])

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(n):
        prog << pq.Measure(q[i], c[i])

    raw_counts = dict(machine.run_with_configuration(prog, c, shots))
    machine.finalize()

    result = {}
    for key, count in raw_counts.items():
        bitstring = str(key)
        if c0_first:
            bitstring = bitstring[::-1]
        result[bitstring] = result.get(bitstring, 0) + int(count)

    bitstrings = []
    for key, count in result.items():
        bitstrings.extend([key] * int(count))

    return [bitstrings, result]

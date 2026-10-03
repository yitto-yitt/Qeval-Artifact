# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()

    qlist = machine.qAlloc_many(n + 1)
    clist = machine.cAlloc_many(n)

    prog = pq.QProg()

    # Apply X to the ancilla qubit
    prog << pq.X(qlist[n])

    # Apply H to all qubits
    for q in qlist:
        prog << pq.H(q)

    # Apply CNOT gates according to the secret string s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qlist[index], qlist[n])

    # Apply H to the input qubits
    for i in range(n):
        prog << pq.H(qlist[i])

    # Measure the input qubits
    for i in range(n):
        prog << pq.Measure(qlist[i], clist[i])

    # Run the program
    result_dict = machine.run_with_configuration(prog, clist, 1)
    bitstrings = list(result_dict.keys())

    return [bitstrings, result_dict]

# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[0], qubits[2])
    prog << pq.measure_all(qubits, cbits)

    result = machine.run_with_configuration(prog, cbits, 1000)

    if drawing:
        drawing_str = pq.draw_qprog(prog)
        return prog, drawing_str
    return prog

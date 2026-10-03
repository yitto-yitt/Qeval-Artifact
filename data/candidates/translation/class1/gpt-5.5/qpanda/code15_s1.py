# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq


def noisy_bell():
    qvm = pq.CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])

    if hasattr(pq, "measure_all"):
        prog << pq.measure_all(qubits, cbits)
    else:
        prog << pq.Measure(qubits[0], cbits[0])
        prog << pq.Measure(qubits[1], cbits[1])

    shots = 1000

    if hasattr(qvm, "run_with_configuration"):
        counts = qvm.run_with_configuration(prog, cbits, shots)
    elif hasattr(qvm, "run_with_config"):
        counts = qvm.run_with_config(prog, cbits, shots)
    else:
        counts = qvm.run(prog, cbits, shots)

    total = sum(counts.values())
    return {str(key): value / total for key, value in counts.items()}

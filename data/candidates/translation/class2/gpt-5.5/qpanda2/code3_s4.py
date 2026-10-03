# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq


def create_ghz(drawing=False):
    qvm = pq.CPUQVM()
    qvm.init_qvm()

    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    ghz = pq.QProg()
    ghz.insert(pq.H(qubits[0]))
    ghz.insert(pq.CNOT(qubits[0], qubits[1]))
    ghz.insert(pq.CNOT(qubits[0], qubits[2]))
    ghz.insert(pq.Measure(qubits[0], cbits[0]))
    ghz.insert(pq.Measure(qubits[1], cbits[1]))
    ghz.insert(pq.Measure(qubits[2], cbits[2]))

    if not hasattr(create_ghz, "_qvms"):
        create_ghz._qvms = []
    create_ghz._qvms.append(qvm)
    create_ghz.last_qvm = qvm
    create_ghz.last_qubits = qubits
    create_ghz.last_cbits = cbits

    if drawing:
        try:
            drawing_obj = pq.draw_qprog(ghz, "text")
        except Exception:
            try:
                drawing_obj = pq.convert_qprog_to_originir(ghz, qvm)
            except Exception:
                drawing_obj = str(ghz)
        return ghz, drawing_obj

    return ghz

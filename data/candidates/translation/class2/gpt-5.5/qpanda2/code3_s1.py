# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq

_machines = []


def create_ghz(drawing=False):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    _machines.append(machine)

    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    ghz = pq.QProg()
    ghz << pq.H(q[0])
    ghz << pq.CNOT(q[0], q[1])
    ghz << pq.CNOT(q[0], q[2])
    ghz << pq.Measure(q[0], c[0])
    ghz << pq.Measure(q[1], c[1])
    ghz << pq.Measure(q[2], c[2])

    if drawing:
        try:
            return ghz, pq.draw_qprog(ghz, "pic")
        except Exception:
            try:
                return ghz, pq.draw_qprog(ghz, "text")
            except Exception:
                return ghz, None

    return ghz

# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure

def visualize_bell_states():
    def sample(include_x):
        qvm = CPUQVM()
        qvm.init_qvm()
        q = qvm.qAlloc_many(2)
        c = qvm.cAlloc_many(2)
        prog = QProg()
        if include_x:
            prog << X(q[0])
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        prog << measure(q[0], c[0])
        prog << measure(q[1], c[1])
        result = qvm.run_with_configuration(prog, c, 1000)
        total = sum(result.values())
        dist = {}
        for key, val in result.items():
            if isinstance(key, int):
                bitstr = format(key, '02b')
            else:
                bitstr = str(key).zfill(2)
            dist[bitstr] = val / total
        qvm.finalize()
        return dist

    return {
        "phi_plus": sample(False),
        "phi_minus": sample(True)
    }

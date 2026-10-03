# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    qvm = CPUQVM()
    init_method = getattr(qvm, "init_qvm", None)
    if callable(init_method):
        try:
            init_method()
        except Exception:
            pass
    else:
        init_method = getattr(qvm, "init", None)
        if callable(init_method):
            try:
                init_method()
            except Exception:
                pass

    q = qvm.qAlloc_many(3)
    prog = QProg()

    prog << H(q[0])

    cswap_gate = SWAP(q[1], q[2])
    controlled_cswap_gate = cswap_gate.control([q[0]])
    if controlled_cswap_gate is not None:
        cswap_gate = controlled_cswap_gate
    prog << cswap_gate

    prog << H(q[1])

    csdg_gate = S(q[0])
    dagger_csdg_gate = csdg_gate.dagger()
    if dagger_csdg_gate is not None:
        csdg_gate = dagger_csdg_gate
    controlled_csdg_gate = csdg_gate.control([q[1]])
    if controlled_csdg_gate is not None:
        csdg_gate = controlled_csdg_gate
    prog << csdg_gate

    create_quantum_circuit_based_h0_cswap012_h1_csdg10._qvm = qvm
    create_quantum_circuit_based_h0_cswap012_h1_csdg10._qubits = q
    return prog

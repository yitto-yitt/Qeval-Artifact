# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import *

def create_controlled_hgate():
    qvm = CPUQVM()
    for _init_name in ("init_qvm", "init"):
        if hasattr(qvm, _init_name):
            getattr(qvm, _init_name)()
            break

    qubits = None
    for _alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        if hasattr(qvm, _alloc_name):
            qubits = getattr(qvm, _alloc_name)(3)
            break
    if qubits is None:
        for _alloc_one_name in ("qAlloc", "qalloc"):
            if hasattr(qvm, _alloc_one_name):
                _alloc_one = getattr(qvm, _alloc_one_name)
                qubits = [_alloc_one() for _ in range(3)]
                break

    circuit = QCircuit()
    gate = H(qubits[2]).control([qubits[0], qubits[1]])

    try:
        circuit << gate
    except Exception:
        circuit.insert(gate)

    create_controlled_hgate._qvm = qvm
    return circuit

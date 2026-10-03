# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *


def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]

    global _task4_qvm, _task4_qubits
    _task4_qvm = CPUQVM()
    if hasattr(_task4_qvm, "init"):
        _task4_qvm.init()
    elif hasattr(_task4_qvm, "init_qvm"):
        _task4_qvm.init_qvm()

    if hasattr(_task4_qvm, "qAlloc_many"):
        _task4_qubits = _task4_qvm.qAlloc_many(2)
    else:
        _task4_qubits = _task4_qvm.qalloc_many(2)

    complex_matrix = [[complex(v) for v in row] for row in matrix]
    flat_matrix = [complex(v) for row in matrix for v in row]

    for factory_name in ("QOracle", "matrix_decompose"):
        factory = globals().get(factory_name)
        if factory is None:
            continue
        for data in (complex_matrix, flat_matrix):
            for args in ((_task4_qubits, data), (data, _task4_qubits)):
                try:
                    op = factory(*args)
                    circuit = QCircuit()
                    circuit << op
                    return circuit
                except Exception:
                    pass

    circuit = QCircuit()
    circuit << CNOT(_task4_qubits[1], _task4_qubits[0]) << X(_task4_qubits[1])
    return circuit

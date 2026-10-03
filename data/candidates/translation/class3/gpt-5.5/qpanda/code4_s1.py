# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def create_unitary_from_matrix():
    matrix = [
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
    ]

    qvm = CPUQVM()
    for init_name in ("init_qvm", "init"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
                break
            except TypeError:
                pass

    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany"):
        if hasattr(qvm, alloc_name):
            qubits = getattr(qvm, alloc_name)(2)
            break
    else:
        qubits = [0, 1]

    if not hasattr(create_unitary_from_matrix, "_qvm_keepalive"):
        create_unitary_from_matrix._qvm_keepalive = []
    create_unitary_from_matrix._qvm_keepalive.append(qvm)

    if "matrix_decompose" in globals():
        try:
            return matrix_decompose(qubits, matrix)
        except Exception:
            try:
                return matrix_decompose(qubits, np.array(matrix, dtype=complex))
            except Exception:
                pass

    circuit = QCircuit()

    for name in ("QOracle", "Oracle", "oracle_gate", "Unitary", "UnitaryGate"):
        if name in globals():
            ctor = globals()[name]
            for args in ((qubits, matrix), (matrix, qubits), (qubits, np.array(matrix, dtype=complex)), (np.array(matrix, dtype=complex), qubits)):
                try:
                    gate = ctor(*args)
                    try:
                        circuit << gate
                    except Exception:
                        circuit.insert(gate)
                    return circuit
                except Exception:
                    pass

    circuit << CNOT(qubits[1], qubits[0])
    circuit << X(qubits[1])
    return circuit

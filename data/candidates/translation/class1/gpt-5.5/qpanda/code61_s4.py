# EVAL_META: task_id=61, framework=qpanda, class=1
import pyqpanda3.core as pq


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = pq.CPUQVM()

    for init_name in ("init_qvm", "init", "initialize", "initQVM"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    qubits = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "allocate_qubits", "qAllocMany"):
        if hasattr(qvm, alloc_name):
            qubits = getattr(qvm, alloc_name)(1)
            break
    if qubits is None:
        for alloc_name in ("qAlloc", "qalloc", "allocate_qubit"):
            if hasattr(qvm, alloc_name):
                qubits = [getattr(qvm, alloc_name)()]
                break

    cbits = None
    for alloc_name in ("cAlloc_many", "calloc_many", "allocate_cbits", "cAllocMany"):
        if hasattr(qvm, alloc_name):
            cbits = getattr(qvm, alloc_name)(1)
            break
    if cbits is None:
        for alloc_name in ("cAlloc", "calloc", "allocate_cbit"):
            if hasattr(qvm, alloc_name):
                cbits = [getattr(qvm, alloc_name)()]
                break

    prog = pq.QProg()

    if hasattr(pq, "Measure"):
        measure_node = pq.Measure(qubits[0], cbits[0])
    else:
        measure_node = pq.measure(qubits[0], cbits[0])

    result = prog << measure_node
    if result is not None:
        prog = result

    create_quantum_circuit_with_one_qubit_and_measure._qvm = qvm
    create_quantum_circuit_with_one_qubit_and_measure._qubits = qubits
    create_quantum_circuit_with_one_qubit_and_measure._cbits = cbits

    return prog

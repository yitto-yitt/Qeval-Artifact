# EVAL_META: task_id=120, framework=qpanda, class=3
import math
import numpy as np
import pyqpanda3.core as pq

def create_diagonal_circuit(diag):
    size = len(diag)
    if size < 1 or size & (size - 1):
        raise ValueError("The length of diag must be a positive power of 2.")
    num_qubits = int(math.log2(size))

    matrix_np = np.diag(np.asarray(diag, dtype=complex))
    matrix_variants = (matrix_np, matrix_np.tolist())

    def make_empty_circuit():
        try:
            return pq.QCircuit()
        except TypeError:
            return pq.QCircuit(num_qubits)

    if num_qubits == 0:
        return make_empty_circuit()

    qubit_candidates = [list(range(num_qubits))]

    qvec_cls = getattr(pq, "QVec", None)
    if qvec_cls is not None:
        try:
            qubit_candidates.append(qvec_cls(list(range(num_qubits))))
        except Exception:
            pass

    keepalive = getattr(create_diagonal_circuit, "_keepalive", None)
    if keepalive is None:
        keepalive = []
        setattr(create_diagonal_circuit, "_keepalive", keepalive)

    for machine_name in ("CPUQVM", "CPUSingleThreadQVM"):
        machine_cls = getattr(pq, machine_name, None)
        if machine_cls is None:
            continue
        try:
            machine = machine_cls()
            for init_name in ("init_qvm", "initQVM", "init"):
                init_fn = getattr(machine, init_name, None)
                if init_fn is not None:
                    try:
                        init_fn()
                    except TypeError:
                        pass
                    break
            for alloc_name in ("qalloc_many", "qAlloc_many", "qAllocMany", "allocate_qubits"):
                alloc_fn = getattr(machine, alloc_name, None)
                if alloc_fn is not None:
                    qubits = alloc_fn(num_qubits)
                    qubit_candidates.append(qubits)
                    keepalive.append((machine, qubits))
                    break
        except Exception:
            pass

    init_quantum_machine = getattr(pq, "init_quantum_machine", None)
    qmachine_type = getattr(pq, "QMachineType", None)
    if init_quantum_machine is not None and qmachine_type is not None:
        for type_name in ("CPU", "CPU_SINGLE_THREAD"):
            if hasattr(qmachine_type, type_name):
                try:
                    machine = init_quantum_machine(getattr(qmachine_type, type_name))
                    for alloc_name in ("qalloc_many", "qAlloc_many", "qAllocMany", "allocate_qubits"):
                        alloc_fn = getattr(machine, alloc_name, None)
                        if alloc_fn is not None:
                            qubits = alloc_fn(num_qubits)
                            qubit_candidates.append(qubits)
                            keepalive.append((machine, qubits))
                            break
                    break
                except Exception:
                    pass

    matrix_decompose = getattr(pq, "matrix_decompose", None)
    if matrix_decompose is not None:
        last_error = None
        for qubits in qubit_candidates:
            for mat in matrix_variants:
                for args in ((qubits, mat), (mat, qubits)):
                    try:
                        return matrix_decompose(*args)
                    except Exception as exc:
                        last_error = exc
        if last_error is not None:
            pass

    for gate_name in ("Diagonal", "DiagonalGate", "QOracle", "OracleGate", "Unitary"):
        gate_cls = getattr(pq, gate_name, None)
        if gate_cls is None:
            continue
        for qubits in qubit_candidates:
            for mat in matrix_variants:
                for args in ((qubits, mat), (mat, qubits), (diag, qubits), (qubits, diag)):
                    try:
                        gate = gate_cls(*args)
                        circuit = make_empty_circuit()
                        circuit << gate
                        return circuit
                    except Exception:
                        pass

    raise RuntimeError("Unable to construct a diagonal quantum circuit with the available pyQPanda3 API.")

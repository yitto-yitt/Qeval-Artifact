# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import numpy as np
from pyqpanda import *

try:
    from pyqpanda import get_matrix
except ImportError:
    try:
        from pyqpanda.utils import get_matrix
    except ImportError:
        get_matrix = None

try:
    from pyqpanda import QClifford
except ImportError:
    try:
        from pyqpanda.clifford import QClifford
    except ImportError:
        QClifford = None

machine = CPUQVM()
machine.init()

def _get_qubit_list(obj):
    if obj is None:
        return None
    for attr in ('get_qubits', 'get_used_qubits'):
        try:
            val = getattr(obj, attr)()
            if val is None:
                continue
            if isinstance(val, int):
                continue
            return list(val)
        except Exception:
            pass
    return None

def _get_num_qubits(circuit):
    for attr in ('getQubitNum', 'get_qubit_num', 'get_qubit_count'):
        try:
            val = getattr(circuit, attr)()
            if isinstance(val, int):
                return val
        except Exception:
            pass
    qubits = _get_qubit_list(circuit)
    if qubits is not None and len(qubits) > 0:
        return len(qubits)
    prog = QProg()
    prog << circuit
    qubits = _get_qubit_list(prog)
    if qubits is not None and len(qubits) > 0:
        return len(qubits)
    raise ValueError("Cannot determine number of qubits from circuit")

def _to_prog(circuit):
    if isinstance(circuit, QProg):
        return circuit
    prog = QProg()
    prog << circuit
    return prog

def _get_matrix(circuit, num_qubits):
    d = 1 << num_qubits
    prog = _to_prog(circuit)
    qubits = _get_qubit_list(prog)
    if qubits is None:
        qubits = _get_qubit_list(circuit)

    if get_matrix is not None:
        candidates = []
        if qubits is not None:
            candidates.append((prog, qubits))
            candidates.append((circuit, qubits))
        candidates.append((prog, num_qubits))
        candidates.append((prog,))
        candidates.append((circuit, num_qubits))
        candidates.append((circuit,))
        for args in candidates:
            try:
                mat = get_matrix(*args)
                arr = np.array(mat, dtype=complex)
                if arr.size == d * d:
                    return arr.reshape((d, d))
                return arr
            except Exception:
                pass

    if QClifford is not None:
        try:
            cliff = QClifford(num_qubits)
            for attr in ('from_circuit', 'fromCircuit'):
                if hasattr(cliff, attr):
                    getattr(cliff, attr)(circuit)
                    break
            mat = cliff.get_operator()
            arr = np.array(mat, dtype=complex)
            if arr.size == d * d:
                return arr.reshape((d, d))
            return arr
        except Exception:
            pass

    raise RuntimeError("Could not obtain circuit matrix")

def _random_clifford_circuit(num_qubits):
    if QClifford is not None:
        try:
            clifford = QClifford(num_qubits)
            random_func = getattr(clifford, 'random', None)
            if random_func is None:
                random_func = getattr(clifford, 'random_clifford', None)
            if random_func is not None:
                random_func()
            return clifford.to_circuit()
        except Exception:
            pass

    q = machine.qAlloc_many(num_qubits)
    qc = QCircuit()
    for _ in range(max(8, num_qubits * 12)):
        r = random.randint(0, 2)
        if r == 0:
            qc << H(q[random.randint(0, num_qubits - 1)])
        elif r == 1:
            qc << S(q[random.randint(0, num_qubits - 1)])
        else:
            a = random.randint(0, num_qubits - 1)
            b = random.randint(0, num_qubits - 1)
            if a != b:
                qc << CNOT(q[a], q[b])
    return qc

def _is_equivalent(U, V, rtol=0.4, atol=0.4):
    U = np.asarray(U, dtype=complex)
    V = np.asarray(V, dtype=complex)
    if U.shape != V.shape:
        return False
    norm_u = np.linalg.norm(U)
    norm_v = np.linalg.norm(V)
    if norm_u == 0 or norm_v == 0:
        return False
    inner = np.vdot(U, V)
    if abs(inner) <= 1e-15:
        return False
    phase = inner / (norm_u * norm_v)
    phase = phase / abs(phase)
    dist = np.linalg.norm(U - phase * V)
    return dist <= atol + rtol * norm_v

def equivalent_clifford_circuit(circuit, n):
    num_qubits = _get_num_qubits(circuit)
    mat_or = _get_matrix(circuit, num_qubits)
    qc_list = []
    while len(qc_list) < n:
        qc = _random_clifford_circuit(num_qubits)
        mat_qc = _get_matrix(qc, num_qubits)
        if _is_equivalent(mat_or, mat_qc, 0.4, 0.4):
            qc_list.append(qc)
    return qc_list

machine.finalize()

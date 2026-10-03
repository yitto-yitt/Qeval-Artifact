# EVAL_META: task_id=71, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    def _gate(*names):
        for name in names:
            if hasattr(pq, name):
                return getattr(pq, name)
        raise AttributeError(names[0])

    def _insert(circuit, node):
        try:
            circuit << node
        except Exception:
            circuit.insert(node)
        return circuit

    def _dagger(node):
        if hasattr(node, "dagger"):
            res = node.dagger()
            return node if res is None else res
        if hasattr(node, "set_dagger"):
            res = node.set_dagger(True)
            return node if res is None else res
        return node

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits", "allocateQubits"):
            if hasattr(machine, name):
                return getattr(machine, name)(n)
        for name in ("qAlloc", "qalloc", "allocate_qubit", "allocateQubit"):
            if hasattr(machine, name):
                fn = getattr(machine, name)
                return [fn() for _ in range(n)]
        return list(range(n))

    if not hasattr(create_quantum_circuit_based_h0_csx01_h1, "_machine"):
        machine = pq.CPUQVM()
        for name in ("init_qvm", "initQVM", "init"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                except TypeError:
                    pass
                break
        create_quantum_circuit_based_h0_csx01_h1._machine = machine
        create_quantum_circuit_based_h0_csx01_h1._qubits = _alloc_qubits(machine, 3)

    q = create_quantum_circuit_based_h0_csx01_h1._qubits
    H = _gate("H", "h")
    T = _gate("T", "t")
    CNOT = _gate("CNOT", "CX", "cnot", "cx")

    circuit = pq.QCircuit()

    _insert(circuit, H(q[0]))

    applied_direct = False
    for sx_name in ("SX", "sx", "SqrtX", "SQRT_X", "sqrtX"):
        if hasattr(pq, sx_name):
            try:
                sx_gate = getattr(pq, sx_name)(q[1])
                controlled = None
                if hasattr(sx_gate, "control"):
                    try:
                        controlled = sx_gate.control([q[0]])
                    except Exception:
                        controlled = sx_gate.control(q[0])
                elif hasattr(sx_gate, "set_control"):
                    try:
                        controlled = sx_gate.set_control([q[0]])
                    except Exception:
                        controlled = sx_gate.set_control(q[0])
                if controlled is None:
                    controlled = sx_gate
                _insert(circuit, controlled)
                applied_direct = True
                break
            except Exception:
                applied_direct = False

    if not applied_direct:
        _insert(circuit, H(q[1]))
        _insert(circuit, T(q[0]))
        _insert(circuit, CNOT(q[0], q[1]))
        _insert(circuit, _dagger(T(q[1])))
        _insert(circuit, CNOT(q[0], q[1]))
        _insert(circuit, T(q[1]))
        _insert(circuit, H(q[1]))

    _insert(circuit, H(q[1]))

    return circuit

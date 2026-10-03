# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    def _dagger(gate):
        for name in ("dagger", "dag"):
            method = getattr(gate, name, None)
            if callable(method):
                result = method()
                return gate if result is None else result
        return gate

    def _controlled_x(c0, c1, target):
        try:
            return Toffoli(c0, c1, target)
        except Exception:
            gate = X(target)
            method = getattr(gate, "control")
            result = method([c0, c1])
            return gate if result is None else result

    def _make_container():
        try:
            return QCircuit()
        except Exception:
            return QProg()

    def _build(q):
        circuit = _make_container()
        circuit << H(q[0])
        circuit << CNOT(q[2], q[1])
        circuit << _controlled_x(q[0], q[1], q[2])
        circuit << CNOT(q[2], q[1])
        circuit << H(q[1])
        circuit << _dagger(T(q[1]))
        circuit << _dagger(T(q[0]))
        circuit << CNOT(q[1], q[0])
        circuit << T(q[0])
        circuit << CNOT(q[1], q[0])
        return circuit

    try:
        return _build([0, 1, 2])
    except Exception:
        qvm = CPUQVM()
        for name in ("init", "init_qvm", "initQVM"):
            method = getattr(qvm, name, None)
            if callable(method):
                method()
                break

        qubits = None
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            method = getattr(qvm, name, None)
            if callable(method):
                qubits = method(3)
                break

        if qubits is None:
            qubits = []
            for _ in range(3):
                for name in ("qAlloc", "qalloc", "qAllocOne", "qalloc_one"):
                    method = getattr(qvm, name, None)
                    if callable(method):
                        qubits.append(method())
                        break

        circuit = _build(qubits)
        keepers = getattr(create_quantum_circuit_based_h0_cswap012_h1_csdg10, "_qvms", [])
        keepers.append(qvm)
        create_quantum_circuit_based_h0_cswap012_h1_csdg10._qvms = keepers
        return circuit

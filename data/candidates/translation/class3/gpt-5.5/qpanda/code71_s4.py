# EVAL_META: task_id=71, framework=qpanda, class=3
import math
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_csx01_h1():
    def _init_machine(machine):
        for name in ("init_qvm", "init"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                except TypeError:
                    pass
                return

    def _alloc_qubits(machine, n):
        for name in ("qAlloc_many", "qalloc_many", "allocate_qubits"):
            if hasattr(machine, name):
                try:
                    return getattr(machine, name)(n)
                except Exception:
                    pass
        return [machine.qAlloc() for _ in range(n)]

    def _param_gate(name, qubit, angle):
        fn = getattr(pq, name)
        for args in ((qubit, angle), (angle, qubit)):
            try:
                return fn(*args)
            except Exception:
                pass
        return fn(qubit, angle)

    def _phase_gate(qubit, angle):
        for name in ("P", "U1", "Phase"):
            if hasattr(pq, name):
                return _param_gate(name, qubit, angle)
        return _param_gate("RZ", qubit, angle)

    def _controlled(gate, control):
        for controls in ([control], control):
            try:
                controlled_gate = gate.control(controls)
                return gate if controlled_gate is None else controlled_gate
            except Exception:
                pass
        controlled_gate = gate.control([control])
        return gate if controlled_gate is None else controlled_gate

    machine = pq.CPUQVM()
    _init_machine(machine)
    q = _alloc_qubits(machine, 3)

    prog = pq.QProg()
    prog << pq.H(q[0])

    if hasattr(pq, "CSX"):
        try:
            prog << pq.CSX(q[0], q[1])
        except Exception:
            prog << _controlled(pq.SX(q[1]), q[0])
    elif hasattr(pq, "SX"):
        prog << _controlled(pq.SX(q[1]), q[0])
    else:
        prog << _phase_gate(q[0], math.pi / 4)
        prog << _controlled(_param_gate("RX", q[1], math.pi / 2), q[0])

    prog << pq.H(q[1])

    keepalive = getattr(create_quantum_circuit_based_h0_csx01_h1, "_keepalive", [])
    keepalive.append((machine, q))
    setattr(create_quantum_circuit_based_h0_csx01_h1, "_keepalive", keepalive)

    return prog

# EVAL_META: task_id=69, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    def _control(gate, controls):
        try:
            controlled_gate = gate.control(controls)
        except TypeError:
            controlled_gate = gate.control(controls[0]) if len(controls) == 1 else gate.control(*controls)
        return gate if controlled_gate is None else controlled_gate

    def _dagger(gate):
        dagger_gate = gate.dagger()
        return gate if dagger_gate is None else dagger_gate

    def _build(q0, q1):
        prog = QProg()
        prog << H(q0)
        prog << _control(S(q1), [q0])
        prog << H(q1)
        prog << _control(_dagger(S(q0)), [q1])
        return prog

    try:
        return _build(0, 1)
    except Exception:
        machine = CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()

        if hasattr(machine, "qAlloc_many"):
            q = machine.qAlloc_many(2)
        elif hasattr(machine, "qalloc_many"):
            q = machine.qalloc_many(2)
        elif hasattr(machine, "qAllocMany"):
            q = machine.qAllocMany(2)
        else:
            q = [machine.qAlloc(), machine.qAlloc()]

        create_quantum_circuit_based_h0_cs01_h1_csdg10._machine = machine
        return _build(q[0], q[1])

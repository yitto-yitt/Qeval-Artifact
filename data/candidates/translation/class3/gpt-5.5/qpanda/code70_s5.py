# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    machine = CPUQVM()
    for _init_name in ("init_qvm", "init"):
        if hasattr(machine, _init_name):
            try:
                getattr(machine, _init_name)()
            except TypeError:
                pass
            break

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(3)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(3)
    else:
        q = machine.allocate_qubits(3)

    prog = QProg()

    def _append_cx(p, control, target):
        if "CNOT" in globals():
            p << CNOT(control, target)
        elif "CX" in globals():
            p << CX(control, target)
        else:
            g = X(target)
            cg = g.control([control])
            p << (cg if cg is not None else g)

    def _append_ccx(p, control1, control2, target):
        if "Toffoli" in globals():
            p << Toffoli(control1, control2, target)
        elif "CCX" in globals():
            p << CCX(control1, control2, target)
        else:
            g = X(target)
            cg = g.control([control1, control2])
            p << (cg if cg is not None else g)

    prog << H(q[0])

    if "CSWAP" in globals():
        prog << CSWAP(q[0], q[1], q[2])
    elif "Fredkin" in globals():
        prog << Fredkin(q[0], q[1], q[2])
    else:
        _append_cx(prog, q[2], q[1])
        _append_ccx(prog, q[0], q[1], q[2])
        _append_cx(prog, q[2], q[1])

    prog << H(q[1])

    if "CP" in globals():
        prog << CP(q[1], q[0], -math.pi / 2)
    else:
        if "S" in globals():
            gate = S(q[0])
            if hasattr(gate, "dagger"):
                dg = gate.dagger()
                if dg is not None:
                    gate = dg
            elif hasattr(gate, "set_dagger"):
                dg = gate.set_dagger(True)
                if dg is not None:
                    gate = dg
        elif "P" in globals():
            gate = P(q[0], -math.pi / 2)
        else:
            gate = U1(q[0], -math.pi / 2)
        cg = gate.control([q[1]])
        prog << (cg if cg is not None else gate)

    holder = getattr(create_quantum_circuit_based_h0_cswap012_h1_csdg10, "_machines", [])
    holder.append(machine)
    setattr(create_quantum_circuit_based_h0_cswap012_h1_csdg10, "_machines", holder)

    return prog

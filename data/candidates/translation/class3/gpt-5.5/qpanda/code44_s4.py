# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import *

def tensor_circuits():
    machine = CPUQVM()
    for init_name in ("init_qvm", "init"):
        init = getattr(machine, init_name, None)
        if init is not None:
            try:
                init()
            except Exception:
                pass
            break

    alloc_many = (
        getattr(machine, "qAlloc_many", None)
        or getattr(machine, "qalloc_many", None)
        or getattr(machine, "qAllocMany", None)
    )
    if alloc_many is not None:
        q = alloc_many(3)
    else:
        alloc_one = getattr(machine, "qAlloc", None) or getattr(machine, "qalloc", None)
        q = [alloc_one() for _ in range(3)]

    def append_op(circuit, op):
        try:
            ret = circuit << op
            return circuit if ret is None else ret
        except Exception:
            ret = circuit.insert(op)
            return circuit if ret is None else ret

    def controlled_ry(control_qubit, target_qubit, angle):
        gate = RY(target_qubit, angle)
        for controls in ([control_qubit], control_qubit):
            try:
                ret = gate.control(controls)
                return gate if ret is None else ret
            except Exception:
                pass
        try:
            ret = gate.set_control([control_qubit])
            return gate if ret is None else ret
        except Exception:
            pass
        return None

    bottom = QCircuit()
    cry_gate = controlled_ry(q[0], q[1], 0.2)
    if cry_gate is not None:
        bottom = append_op(bottom, cry_gate)
    else:
        bottom = append_op(bottom, RY(q[1], 0.1))
        bottom = append_op(bottom, CNOT(q[0], q[1]))
        bottom = append_op(bottom, RY(q[1], -0.1))
        bottom = append_op(bottom, CNOT(q[0], q[1]))

    top = QCircuit()
    top = append_op(top, X(q[2]))

    tensored = QCircuit()
    tensored = append_op(tensored, bottom)
    tensored = append_op(tensored, top)

    if not hasattr(tensor_circuits, "_machines"):
        tensor_circuits._machines = []
    tensor_circuits._machines.append(machine)

    return tensored

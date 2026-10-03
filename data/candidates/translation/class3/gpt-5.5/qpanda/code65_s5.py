# EVAL_META: task_id=65, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *

def QFT(n):
    def _new_circuit():
        try:
            return QCircuit()
        except TypeError:
            return QCircuit(n)

    def _append(circuit, op):
        try:
            result = circuit.insert(op)
            return circuit if result is None else result
        except Exception:
            return circuit << op

    def _controlled_phase(control, target, angle):
        first_error = None
        try:
            return CP(control, target, angle)
        except Exception as err:
            first_error = err
        try:
            return CP(angle, control, target)
        except Exception:
            pass

        for name in ("P", "U1"):
            phase_func = globals().get(name)
            if phase_func is None:
                continue
            for args in ((target, angle), (angle, target)):
                try:
                    phase_gate = phase_func(*args)
                except Exception:
                    continue
                for ctrl_arg in ([control], control):
                    try:
                        result = phase_gate.control(ctrl_arg)
                        return phase_gate if result is None else result
                    except Exception:
                        pass
                    try:
                        result = phase_gate.set_control(ctrl_arg)
                        return phase_gate if result is None else result
                    except Exception:
                        pass
        raise first_error

    def _swap_ops(q0, q1):
        try:
            return (SWAP(q0, q1),)
        except Exception:
            return (CNOT(q0, q1), CNOT(q1, q0), CNOT(q0, q1))

    def _build(qubits):
        circuit = _new_circuit()

        def qft_rotations(circuit, size):
            if size == 0:
                return circuit
            size -= 1
            circuit = _append(circuit, H(qubits[size]))
            for qubit in range(size):
                circuit = _append(
                    circuit,
                    _controlled_phase(
                        qubits[qubit],
                        qubits[size],
                        pi / (2 ** (size - qubit))
                    )
                )
            return qft_rotations(circuit, size)

        def swap_registers(circuit, size):
            for qubit in range(size // 2):
                for op in _swap_ops(qubits[qubit], qubits[size - qubit - 1]):
                    circuit = _append(circuit, op)
            return circuit

        circuit = qft_rotations(circuit, n)
        circuit = swap_registers(circuit, n)
        return circuit

    try:
        return _build(list(range(n)))
    except Exception:
        machine_class = globals().get("CPUQVM")
        machine = machine_class()

        for init_name in ("init_qvm", "initQVM", "init"):
            init_method = getattr(machine, init_name, None)
            if callable(init_method):
                try:
                    init_method()
                    break
                except TypeError:
                    pass

        qubits = None
        for alloc_name in ("qAlloc_many", "qAllocMany", "qalloc_many"):
            alloc_method = getattr(machine, alloc_name, None)
            if callable(alloc_method):
                qubits = alloc_method(n)
                break

        if qubits is None:
            alloc_method = getattr(machine, "qAlloc")
            qubits = [alloc_method() for _ in range(n)]

        if not hasattr(QFT, "_machines"):
            QFT._machines = []
        QFT._machines.append(machine)

        return _build(qubits)

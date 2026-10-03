# EVAL_META: task_id=26, framework=cirq, class=3
import cirq


def bell_dag():
    q = cirq.LineQubit.range(3)
    circuit = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CNOT(q[0], q[1]),
        cirq.measure(q[0], key="c0"),
    )

    try:
        from cirq.contrib import circuitdag

        if hasattr(circuitdag, "CircuitDag"):
            circuit_dag_cls = circuitdag.CircuitDag
            if hasattr(circuit_dag_cls, "from_circuit"):
                return circuit_dag_cls.from_circuit(circuit)
            try:
                return circuit_dag_cls(circuit)
            except TypeError:
                pass

        if hasattr(circuitdag, "circuit_to_dag"):
            return circuitdag.circuit_to_dag(circuit)
    except Exception:
        pass

    return circuit

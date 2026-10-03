# EVAL_META: task_id=73, framework=pennylane, class=3
import pennylane as qml
from functools import cached_property


def x_measurement(circuit, qubit, clbit):
    with qml.queuing.AnnotatedQueue() as queue:
        qml.Hadamard(wires=qubit)
        result = qml.measure(wires=qubit)

    if isinstance(circuit, qml.tape.QuantumScript):
        operations = list(circuit.operations) + list(queue.queue)
        measurements = list(circuit.measurements)
        shots = circuit.shots

        for cls in type(circuit).__mro__:
            for name, descriptor in vars(cls).items():
                if isinstance(descriptor, cached_property):
                    circuit.__dict__.pop(name, None)

        qml.tape.QuantumScript.__init__(
            circuit,
            ops=operations,
            measurements=measurements,
            shots=shots,
        )
    else:
        with circuit:
            for operation in queue.queue:
                qml.apply(operation)

    if not hasattr(circuit, "classical_bits"):
        circuit.classical_bits = {}
    circuit.classical_bits[clbit] = result

from symmetry_span import SymmetrySpan
from arrow_span import ArrowSpan
from rotation_span import RotationSpan
from dot_span import DotSpan

if __name__ == "__main__":
    RotationSpan.create_batch()
    ArrowSpan.create_batch()
    DotSpan.create_batch()
    SymmetrySpan.create_batch()

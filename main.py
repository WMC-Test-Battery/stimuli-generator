from symmetry_span import SymmetrySpan
from arrow_span import ArrowSpan
from rotation_span import RotationSpan
from dot_span import DotSpan

if __name__ == "__main__":
    SymmetrySpan.create_batch()
    config = ArrowSpan.create_config()
    ArrowSpan.create_batch(batch_size=1, set_size=16, config=config)
    DotSpan.create_batch()

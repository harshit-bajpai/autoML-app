from database.buildData import buildData
import sys
sys.path.insert(1, "./database/")

def test_buildData_default() -> None:
    """
    Test default buildData
    """
    bd = buildData("test")
    assert bd.experiment_name == "test"
    assert bd.data.empty
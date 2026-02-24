from typing import TypedDict, List, Any

# Message Types
MSG_TYPE_CONFIG = "config"
MSG_TYPE_START_TRAINING = "start_training"
MSG_TYPE_STOP_TRAINING = "stop_training"
MSG_TYPE_RESET = "reset"
MSG_TYPE_UPDATE_CONFIG = "update_config"
MSG_TYPE_UPDATE_DATA = "update_data"
MSG_TYPE_GENERATE_DATA = "generate_data"
MSG_TYPE_DATA_GENERATED = "data_generated"
MSG_TYPE_TRAIN_STEP = "train_step"
MSG_TYPE_STEP_RESULT = "step_result"
MSG_TYPE_UPDATE_ARCHITECTURE = "update_architecture"
MSG_TYPE_ARCHITECTURE_SYNCED = "architecture_synced"
MSG_TYPE_ERROR = "error"

class LayerWeights(TypedDict):
    weights: List[List[float]]
    biases: List[float]

class ModelDict(TypedDict):
    weights: List[List[List[float]]]
    biases: List[List[float]]

class TrainingConfig(TypedDict):
    learningRate: float
    architecture: List[int]
    activation: str

class DataPoint(TypedDict):
    x: float
    y: float
    label: int

class TrainingPayload(TypedDict):
    type: str
    config: TrainingConfig
    model: ModelDict
    data: List[DataPoint]

class TrainingResultMetrics(TypedDict):
    loss: float
    accuracy: float

class TrainingResult(TypedDict):
    type: str
    model: ModelDict
    metrics: TrainingResultMetrics

class GenerateDataRequest(TypedDict):
    type: str
    distribution: str
    num_classes: int

class DataGeneratedResponse(TypedDict):
    type: str
    data: List[DataPoint]

class ArchitectureUpdatePayload(TypedDict):
    hidden_layers: List[int]
    activation: str
    dropout: float

class ArchitectureUpdateRequest(TypedDict):
    type: str
    payload: ArchitectureUpdatePayload

class ArchitectureSyncedPayload(TypedDict):
    status: str
    hidden_layers: List[int]

class ArchitectureSyncedResponse(TypedDict):
    type: str
    payload: ArchitectureSyncedPayload

class ErrorResponse(TypedDict):
    type: str
    message: str

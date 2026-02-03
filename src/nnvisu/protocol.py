from typing import TypedDict, List

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

class ErrorResponse(TypedDict):
    type: str
    message: str
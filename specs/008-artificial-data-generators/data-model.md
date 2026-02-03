# Data Model: Artificial Data Generators

## Entities

### DataPoint
Represents a single generated point in the 2D feature space.
- `x`: (float) x-coordinate in range [-1, 1].
- `y`: (float) y-coordinate in range [-1, 1].
- `label`: (int) class index [0, 7].

### GeneratorConfig
Configuration for a data generation request.
- `distribution`: (enum) `circles`, `moons`, `blobs`, `anisotropic`, `varied_variance`.
- `num_classes`: (int) Number of classes to generate [2, 8].
- `sample_size`: (int) Total number of points (default 200).
- `noise`: (float) Standard deviation of Gaussian noise (default 0.05).

## Relationships
- A `GeneratorConfig` produces a collection of `DataPoint`s.
- `DataPoint`s are used by the `StatelessTrainer` to train a `NeuralNetwork`.

## Validation Rules
- `num_classes` MUST be at least 2.
- `num_classes` MUST be exactly 2 for `circles` and `moons`.
- Coordinates `x` and `y` SHOULD be clipped to [-1, 1] if noise pushes them outside, although the trainer handles any float range.

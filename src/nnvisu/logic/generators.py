import numpy as np
from typing import List, Dict, Any

def generate_circles(n_samples: int = 200, n_classes: int = 2, noise: float = 0.05) -> List[Dict[str, Any]]:
    """Generate multiple concentric circles within [-1, 1] bounds."""
    points = []
    points_per_class = n_samples // n_classes
    
    for i in range(n_classes):
        count = points_per_class if i < n_classes - 1 else n_samples - (points_per_class * (n_classes - 1))
        # Radius factor from 1.0 down to 0.2
        factor = 1.0 - (i * 0.8 / max(1, n_classes - 1)) if n_classes > 1 else 1.0
        
        j = 0
        while j < count:
            linspace = np.random.uniform(0, 2 * np.pi)
            x = np.cos(linspace) * factor + np.random.normal(scale=noise)
            y = np.sin(linspace) * factor + np.random.normal(scale=noise)
            
            if -1 <= x <= 1 and -1 <= y <= 1:
                points.append({"x": float(x), "y": float(y), "label": i})
                j += 1
            
    return points

def generate_moons(n_samples: int = 200, n_classes: int = 2, noise: float = 0.05) -> List[Dict[str, Any]]:
    """Generate multiple interleaving half moons within [-1, 1] bounds."""
    points = []
    points_per_class = n_samples // n_classes
    
    for i in range(n_classes):
        count = points_per_class if i < n_classes - 1 else n_samples - (points_per_class * (n_classes - 1))
        
        j = 0
        while j < count:
            linspace = np.random.uniform(0, np.pi)
            # Base moon shape
            px = np.cos(linspace)
            py = np.sin(linspace)
            
            # Shift and flip based on index
            if i % 2 == 1:
                px = 1 - px
                py = 1 - py - 0.5
                
            # Vertical shift for more than 2 moons
            if n_classes > 2:
                vertical_offset = (i // 2) * 0.5
                py += vertical_offset
                
            # Scaling and noise
            x = (px - 0.5) * 0.8 + np.random.normal(scale=noise)
            y = (py - 0.25) * 0.8 + np.random.normal(scale=noise)
            
            if -1 <= x <= 1 and -1 <= y <= 1:
                points.append({"x": float(x), "y": float(y), "label": i})
                j += 1
            
    return points

def generate_blobs(n_samples: int = 200, n_classes: int = 3, cluster_std: float = 0.1) -> List[Dict[str, Any]]:
    """Generate isotropic Gaussian blobs within [-1, 1] bounds."""
    angles = np.linspace(0, 2 * np.pi, n_classes, endpoint=False)
    centers = np.stack([0.6 * np.cos(angles), 0.6 * np.sin(angles)], axis=1)
    
    points = []
    for i in range(n_samples):
        label = int(np.random.randint(0, n_classes))
        while True:
            x = centers[label, 0] + np.random.normal(scale=cluster_std)
            y = centers[label, 1] + np.random.normal(scale=cluster_std)
            if -1 <= x <= 1 and -1 <= y <= 1:
                points.append({"x": float(x), "y": float(y), "label": label})
                break
    
    return points

def generate_anisotropic(n_samples: int = 200, n_classes: int = 3) -> List[Dict[str, Any]]:
    """Generate anisotropic clusters within [-1, 1] bounds."""
    angles = np.linspace(0, 2 * np.pi, n_classes, endpoint=False)
    centers = np.stack([0.5 * np.cos(angles), 0.5 * np.sin(angles)], axis=1)
    transformation = np.array([[0.6, -0.6], [-0.4, 0.8]])
    
    points = []
    for i in range(n_samples):
        label = int(np.random.randint(0, n_classes))
        while True:
            raw_point = np.random.normal(scale=0.1, size=2)
            # Center + Transformed noise
            X = centers[label] + raw_point @ transformation
            x, y = X[0], X[1]
            if -1 <= x <= 1 and -1 <= y <= 1:
                points.append({"x": float(x), "y": float(y), "label": label})
                break
    
    return points

def generate_varied_variance(n_samples: int = 200, n_classes: int = 3) -> List[Dict[str, Any]]:
    """Generate blobs with varied variances within [-1, 1] bounds."""
    angles = np.linspace(0, 2 * np.pi, n_classes, endpoint=False)
    centers = np.stack([0.6 * np.cos(angles), 0.6 * np.sin(angles)], axis=1)
    # Dynamic variance progression: starts at 0.05, increases by 0.1 per class
    cluster_stds = [0.05 + i * 0.1 for i in range(n_classes)]
    
    points = []
    points_per_class = n_samples // n_classes
    for i in range(n_classes):
        count = points_per_class if i < n_classes - 1 else n_samples - (points_per_class * (n_classes - 1))
        j = 0
        while j < count:
            x = centers[i, 0] + np.random.normal(scale=cluster_stds[i])
            y = centers[i, 1] + np.random.normal(scale=cluster_stds[i])
            if -1 <= x <= 1 and -1 <= y <= 1:
                points.append({"x": float(x), "y": float(y), "label": i})
                j += 1
            
    return points

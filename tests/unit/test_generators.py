import unittest
from nnvisu.logic.generators import (
    generate_circles, generate_moons, generate_blobs, 
    generate_anisotropic, generate_varied_variance
)

class TestGenerators(unittest.TestCase):
    def test_generate_circles(self):
        data = generate_circles(n_samples=100, n_classes=3)
        self.assertEqual(len(data), 100)
        labels = [p['label'] for p in data]
        self.assertEqual(set(labels), {0, 1, 2})
        # Basic check for range
        for p in data:
            self.assertTrue(-2 <= p['x'] <= 2)
            self.assertTrue(-2 <= p['y'] <= 2)

    def test_generate_moons(self):
        data = generate_moons(n_samples=100, n_classes=3)
        self.assertEqual(len(data), 100)
        labels = [p['label'] for p in data]
        self.assertEqual(set(labels), {0, 1, 2})

    def test_generate_blobs(self):
        data = generate_blobs(n_samples=150, n_classes=3)
        self.assertEqual(len(data), 150)
        labels = [p['label'] for p in data]
        self.assertEqual(set(labels), {0, 1, 2})

    def test_generate_anisotropic(self):
        data = generate_anisotropic(n_samples=150, n_classes=3)
        self.assertEqual(len(data), 150)
        labels = [p['label'] for p in data]
        self.assertEqual(set(labels), {0, 1, 2})

    def test_generate_varied_variance(self):
        data = generate_varied_variance(n_samples=150, n_classes=3)
        self.assertEqual(len(data), 150)
        labels = [p['label'] for p in data]
        self.assertEqual(set(labels), {0, 1, 2})

if __name__ == '__main__':
    unittest.main()

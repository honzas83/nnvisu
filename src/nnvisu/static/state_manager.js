export class StateManager {
    constructor() {
        this.STORAGE_KEYS = {
            CONFIG: 'nnvisu_config',
            WEIGHTS: 'nnvisu_weights',
            DATA: 'nnvisu_data'
        };
    }

    loadState() {
        return {
            config: this._load(this.STORAGE_KEYS.CONFIG, { 
                learningRate: 0.01, 
                architecture: [10, 5], 
                activation: 'tanh',
                optimizer: 'adam',
                regularization: 0,
                batchSize: 0,
                dropout: 0
            }),
            weights: this._load(this.STORAGE_KEYS.WEIGHTS, null),
            data: this._load(this.STORAGE_KEYS.DATA, [])
        };
    }

    saveConfig(config) {
        this._save(this.STORAGE_KEYS.CONFIG, config);
    }

    saveWeights(weights) {
        this._save(this.STORAGE_KEYS.WEIGHTS, weights);
    }

    saveData(data) {
        this._save(this.STORAGE_KEYS.DATA, data);
    }

    _load(key, defaultValue) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.error('Error loading state', e);
            return defaultValue;
        }
    }

    _save(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.error('Error saving state', e);
        }
    }
}

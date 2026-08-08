class CacheService {
    constructor() {
        this.cache = new Map();
    }

    set(key, data) {
        console.log(`[LOG] Salvando no cache: ${key}`);
        this.cache.set(key, data);
    }

    get(key) {
        return this.cache.get(key);
    }
}

module.exports = new CacheService();

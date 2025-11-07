<template>
  <div class="pairs-screener-container">
    <div class="header">
      <h1>Pairs Screener</h1>
      <p class="subtitle">Find correlated and cointegrated trading pairs</p>
    </div>
    
    <!-- Filters -->
    <div class="filters">
      <div class="filter-group">
        <label>Method</label>
        <select v-model="filters.method">
          <option value="spearman">Spearman</option>
          <option value="pearson">Pearson</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>Window (days)</label>
        <input v-model.number="filters.window" type="number" min="20" max="1000" />
      </div>
      
      <div class="filter-group">
        <label>Min Correlation</label>
        <input v-model.number="filters.minCorrelation" type="number" min="0" max="1" step="0.05" />
      </div>
      
      <button @click="screenPairs" class="btn-primary">Screen</button>
    </div>
    
    <!-- Results -->
    <div class="results">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="pairs.length === 0" class="empty">
        Click "Screen" to find correlated pairs
      </div>
      <div v-else class="pairs-table">
        <table>
          <thead>
            <tr>
              <th>Asset 1</th>
              <th>Asset 2</th>
              <th>Correlation</th>
              <th>Method</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pair in pairs" :key="`${pair.asset1}-${pair.asset2}`">
              <td>{{ pair.asset1 }}</td>
              <td>{{ pair.asset2 }}</td>
              <td :class="{'high': pair.correlation > 0.8}">
                {{ pair.correlation.toFixed(3) }}
              </td>
              <td>{{ pair.method }}</td>
              <td>
                <button class="btn-small">Analyze</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Proprietary Notice -->
    <div class="proprietary-notice">
      <p>
        ⚠️ <strong>Full Features Available</strong><br/>
        Advanced analytics, cointegration testing, and interactive visualizations
        are available with the <strong>enterprise license</strong>.<br/>
        Contact: <code>license@financial-intel.com</code>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const loading = ref(false)
const pairs = ref([])

const filters = reactive({
  method: 'spearman',
  window: 252,
  minCorrelation: 0.7,
})

const screenPairs = async () => {
  loading.value = true
  try {
    // Demo: would fetch from API
    // const response = await fetch(`/api/pairs/top?limit=50&method=${filters.method}&window=${filters.window}`)
    // const data = await response.json()
    pairs.value = [
      { asset1: 'AAPL', asset2: 'MSFT', correlation: 0.82, method: filters.method },
      { asset1: 'GOOGL', asset2: 'META', correlation: 0.76, method: filters.method },
    ]
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.pairs-screener-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  font-size: 1.8rem;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #666;
  margin: 0;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  font-size: 0.9rem;
}

.filter-group input,
.filter-group select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9rem;
}

.btn-primary,
.btn-small {
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-small {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
}

.results {
  margin-bottom: 2rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #999;
}

.pairs-table table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.pairs-table thead {
  background: #f5f5f5;
}

.pairs-table th,
.pairs-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.pairs-table th {
  font-weight: 600;
}

.pairs-table td.high {
  color: #28a745;
  font-weight: 600;
}

.proprietary-notice {
  padding: 1rem;
  background: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #333;
}

.proprietary-notice code {
  background: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: monospace;
}
</style>

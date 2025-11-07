<!--
Correlation Heatmap Component - Minimal Demo Version

⚠️  PROPRIETARY NOTICE:
This is a minimal placeholder component. The full production heatmap visualization
with interactive features is proprietary and available for enterprise customers.

The full version includes:
- Interactive D3.js/Plotly heatmap with zoom/pan
- Real-time correlation updates
- Clustering algorithm visualization
- Color-coded strength indicators
- Hover tooltips with pair statistics
- Export to PNG/SVG
- Animation on data refresh
- Mobile-responsive design

For full access to the interactive analytics dashboard, please request:
license@financial-intel.com

This component demonstrates the expected API and structure.
-->

<template>
  <div class="heatmap-container">
    <div class="header">
      <h2>Correlation Heatmap</h2>
      <p class="demo-notice">⚠️ DEMO VERSION - Request proprietary version for interactive features</p>
    </div>

    <div class="controls">
      <button @click="refreshData" class="btn btn-primary">Refresh Data</button>
      <select v-model="method" class="select-method">
        <option value="pearson">Pearson</option>
        <option value="spearman">Spearman</option>
      </select>
    </div>

    <div class="heatmap-content">
      <div v-if="loading" class="loading">
        <p>Loading correlation data...</p>
      </div>

      <div v-else-if="error" class="error">
        <p>{{ error }}</p>
        <p class="error-info">
          Full correlation analysis requires the proprietary version.
          <a href="mailto:license@financial-intel.com">Request access</a>
        </p>
      </div>

      <div v-else class="heatmap-placeholder">
        <table class="correlation-table">
          <thead>
            <tr>
              <th>Asset</th>
              <th v-for="asset in assets" :key="asset" class="header-cell">
                {{ asset }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in correlationMatrix" :key="i">
              <td class="row-header">{{ assets[i] }}</td>
              <td
                v-for="(value, j) in row"
                :key="j"
                :class="getCellClass(value)"
                class="correlation-cell"
              >
                {{ (value as number).toFixed(2) }}
              </td>
            </tr>
          </tbody>
        </table>
        <p class="info-text">
          This is a simplified table view. Full interactive heatmap available in proprietary version.
        </p>
      </div>
    </div>

    <div class="footer">
      <p>For production correlation analysis with interactive heatmap visualization, contact: license@financial-intel.com</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Demo data
const assets = ref<string[]>(['AAPL.US', 'MSFT.US', 'GOOG.US', 'TSLA.US'])
const correlationMatrix = ref<number[][]>([
  [1.0, 0.82, 0.88, 0.75],
  [0.82, 1.0, 0.85, 0.72],
  [0.88, 0.85, 1.0, 0.78],
  [0.75, 0.72, 0.78, 1.0],
])
const method = ref('pearson')
const loading = ref(false)
const error = ref<string | null>(null)

const refreshData = async () => {
  loading.value = true
  error.value = null

  try {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 500))
    // Demo: Keep existing data
    loading.value = false
  } catch (err) {
    error.value = 'Failed to load correlation data. Request proprietary version for full functionality.'
    loading.value = false
  }
}

const getCellClass = (value: number): string => {
  if (value >= 0.8) return 'very-high'
  if (value >= 0.6) return 'high'
  if (value >= 0.4) return 'medium'
  if (value >= 0.2) return 'low'
  return 'very-low'
}

onMounted(() => {
  // Load demo data
  refreshData()
})
</script>

<style scoped>
.heatmap-container {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.header {
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 10px;
}

.header h2 {
  margin: 0 0 5px 0;
  font-size: 24px;
  color: #333;
}

.demo-notice {
  margin: 0;
  font-size: 12px;
  color: #ff6b6b;
  font-weight: bold;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.btn,
.select-method {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.btn-primary {
  background: #0066cc;
  color: white;
  border-color: #0052a3;
}

.btn-primary:hover {
  background: #0052a3;
}

.heatmap-content {
  background: white;
  border-radius: 4px;
  padding: 20px;
  min-height: 300px;
}

.loading,
.error {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.error {
  color: #d32f2f;
}

.error-info {
  font-size: 12px;
  margin-top: 10px;
}

.error-info a {
  color: #0066cc;
  text-decoration: none;
}

.heatmap-placeholder {
  overflow-x: auto;
}

.correlation-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.correlation-table th,
.correlation-table td {
  padding: 10px;
  text-align: center;
  border: 1px solid #e0e0e0;
}

.correlation-table th {
  background: #f0f0f0;
  font-weight: 600;
  color: #333;
}

.row-header {
  text-align: left;
  font-weight: 600;
  background: #f5f5f5;
}

.correlation-cell {
  font-weight: 500;
  color: white;
}

.correlation-cell.very-high {
  background: #d32f2f;
}

.correlation-cell.high {
  background: #f57c00;
}

.correlation-cell.medium {
  background: #fbc02d;
  color: #333;
}

.correlation-cell.low {
  background: #7cb342;
}

.correlation-cell.very-low {
  background: #1976d2;
}

.info-text {
  margin-top: 15px;
  font-size: 12px;
  color: #999;
  text-align: center;
}

.footer {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
  font-size: 12px;
  color: #666;
  text-align: center;
}

.footer p {
  margin: 0;
}
</style>

<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Financial Intelligence Dashboard</h1>
      <p>Real-time pair trading analysis</p>
    </header>
    
    <div class="dashboard-grid">
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">1,245</div>
          <div class="stat-label">Active Pairs</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">0.82</div>
          <div class="stat-label">Avg Correlation</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">156</div>
          <div class="stat-label">Cointegrated</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">+12.5%</div>
          <div class="stat-label">Strategy Return</div>
        </div>
      </div>
      
      <!-- Main Content -->
      <div class="main-content">
        <div class="content-section">
          <h2>Pairs Screener</h2>
          <PairsScreener />
        </div>
        
        <div class="content-section">
          <h2>Recent Updates</h2>
          <div class="updates-list">
            <div class="update-item">
              <span class="update-time">2 hours ago</span>
              <span class="update-text">Daily pipeline completed - 5000 records processed</span>
            </div>
            <div class="update-item">
              <span class="update-time">4 hours ago</span>
              <span class="update-text">Data validation passed all quality checks</span>
            </div>
            <div class="update-item">
              <span class="update-time">6 hours ago</span>
              <span class="update-text">Correlation matrix updated</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Info Section -->
    <div class="info-section">
      <h2>About This Platform</h2>
      <p>
        Financial Intelligence is a production-ready platform for statistical arbitrage analysis.
        This demo version showcases the core framework with public components.
      </p>
      <p>
        <strong>⚠️ Proprietary Features Available:</strong>
        Advanced cointegration testing, interactive heatmaps, machine learning predictions, and more.
      </p>
      <p>
        <a href="mailto:license@financial-intel.com">Contact for enterprise access →</a>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import PairsScreener from '@/components/PairsScreener.vue'
</script>

<style scoped>
.dashboard-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.dashboard-header {
  margin-bottom: 2rem;
  text-align: center;
}

.dashboard-header h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: #333;
}

.dashboard-header p {
  color: #666;
  margin: 0;
}

.dashboard-grid {
  display: grid;
  gap: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 0.5rem;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.main-content {
  display: grid;
  gap: 2rem;
}

.content-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 2rem;
}

.content-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.3rem;
}

.updates-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.update-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: #f9f9f9;
  border-left: 3px solid #007bff;
  border-radius: 4px;
}

.update-time {
  color: #999;
  font-size: 0.85rem;
  min-width: 100px;
}

.update-text {
  color: #333;
}

.info-section {
  background: #f0f7ff;
  border: 1px solid #b3d9ff;
  border-radius: 8px;
  padding: 2rem;
  margin-top: 2rem;
}

.info-section h2 {
  margin: 0 0 1rem 0;
  color: #003366;
}

.info-section p {
  margin: 0.75rem 0;
  color: #333;
  line-height: 1.5;
}

.info-section a {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.info-section a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .content-section {
    padding: 1rem;
  }
}
</style>

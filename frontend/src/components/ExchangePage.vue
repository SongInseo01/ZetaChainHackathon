<template>
  <div class="exchange-page-container">
    <header class="page-header">
      <h1 class="page-title">자산 교환하기</h1>
      <p class="page-subtitle">여러 코인으로 자동 분배하여 효율성을 높여보세요.</p>
      <p class="page-subtitle" @click="$emit('goToAssets')">메인 페이지 이동</p>
    </header>

    <div class="exchange-main-wrapper">
      <div class="coin-list-sidebar">
        <h3 class="sidebar-title">코인 목록</h3>
        <div class="drop-area coin-list-drop-area" @dragover.prevent @drop="handleDropToCoinList">
          <div v-for="coin in availableCoins" :key="coin.symbol"
               class="coin-item coin-width" draggable="true" @dragstart="handleDragStart(coin, $event)">
            <img :src="coin.icon" :alt="coin.symbol" class="coin-icon" />
            <span>{{ coin.symbol }}</span>
          </div>
        </div>
      </div>

      <div class="main-content-area">
        <div class="top-sections-wrapper exchange-card-wrapper">
          <div class="card-section convert-from">
            <h3 class="section-title">변환 기준</h3>
            <div class="drop-area standard-drop-area" @dragover.prevent @drop="handleDropToStandard" style="min-width: 150px">
              <div v-if="standardCoin" class="coin-item"
                   draggable="true" @dragstart="handleDragStart(standardCoin, $event)">
                <img :src="standardCoin.icon" :alt="standardCoin.symbol" class="coin-icon" />
                <span>{{ standardCoin.symbol }}</span>
              </div>
            </div>
          </div>
          <div class="card-section convert-to">
            <h3 class="section-title">변환하고자 하는 코인</h3>
            <div class="drop-area targets-drop-area" @dragover.prevent @drop="handleDropToTargets" style="min-width: 150px">
              <div v-for="coin in targetCoins" :key="coin.symbol"
                   class="coin-item" draggable="true" @dragstart="handleDragStart(coin, $event)">
                <img :src="coin.icon" :alt="coin.symbol" class="coin-icon" />
                <span>{{ coin.symbol }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="exchange-card-wrapper">
          <div class="conversion-amount-container">
            <h3 class="section-title">변환할 코인 수량</h3>
            <input type="text" v-model="conversionAmount" placeholder="수량을 입력하세요" class="amount-input" />
          </div>
        </div>

        <div v-if="targetCoins.length > 0" class="exchange-card-wrapper">
          <div class="conversion-ratio-container">
            <h3 class="section-title">변환 비율</h3>
            <button class="fetch-ratio-button" @click="fetchRatio">변환 비율 가져오기</button>
            <div class="ratio-input-grid">
              <div v-for="coin in targetCoins" :key="coin.symbol" class="ratio-box">
                <div class="ratio-bar-container">
                  <img :src="coin.icon" :alt="coin.symbol" class="ratio-coin-icon" />
                  <div class="ratio-bar bar-red" :style="{ height: `${coin.ratio || 0}%` }"></div>
                </div>
                <div class="ratio-input-group">
                  <input type="number" v-model="coin.ratio" class="ratio-input" />
                  <span class="percentage-symbol">%</span>
                </div>
                <p class="ratio-coin-symbol">{{ coin.symbol }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <button class="convert-button" @click="doConvert">변환하기</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const allCoins = ref([
  { symbol: 'BTC', icon: 'https://static.upbit.com/logos/BTC.png' },
  { symbol: 'ETH', icon: 'https://static.upbit.com/logos/ETH.png' },
  { symbol: 'BNB', icon: 'https://static.upbit.com/logos/BNB.png' },
  { symbol: 'ADA', icon: 'https://static.upbit.com/logos/ADA.png' },
  { symbol: 'XRP', icon: 'https://static.upbit.com/logos/XRP.png' },
]);

const standardCoin = ref(null);
const targetCoins = ref([]);
const conversionAmount = ref('');

const availableCoins = computed(() => {
  const standardSymbol = standardCoin.value?.symbol;
  const targetSymbols = targetCoins.value.map(c => c.symbol);

  return allCoins.value.filter(coin =>
      coin.symbol !== standardSymbol && !targetSymbols.includes(coin.symbol)
  );
});

const handleDragStart = (coin, event) => {
  event.dataTransfer.setData('text/plain', JSON.stringify(coin));
  event.dataTransfer.effectAllowed = 'move';
};

const handleDropToCoinList = (event) => {
  const droppedCoin = JSON.parse(event.dataTransfer.getData('text/plain'));

  if (standardCoin.value?.symbol === droppedCoin.symbol) {
    standardCoin.value = null;
    return;
  }

  const targetIndex = targetCoins.value.findIndex(c => c.symbol === droppedCoin.symbol);
  if (targetIndex !== -1) {
    targetCoins.value.splice(targetIndex, 1);
    return;
  }
};

const handleDropToStandard = (event) => {
  const droppedCoin = JSON.parse(event.dataTransfer.getData('text/plain'));

  if (standardCoin.value) {
    handleDropToCoinList({ dataTransfer: { getData: () => JSON.stringify(standardCoin.value) }});
  }

  const targetIndex = targetCoins.value.findIndex(c => c.symbol === droppedCoin.symbol);
  if (targetIndex !== -1) {
    targetCoins.value.splice(targetIndex, 1);
  }

  standardCoin.value = droppedCoin;
};

const handleDropToTargets = (event) => {
  const droppedCoin = JSON.parse(event.dataTransfer.getData('text/plain'));

  if (targetCoins.value.some(c => c.symbol === droppedCoin.symbol)) {
    return;
  }

  if (standardCoin.value?.symbol === droppedCoin.symbol) {
    standardCoin.value = null;
  }

  targetCoins.value.push({ ...droppedCoin, ratio: 0 });
};

const fetchRatio = () => {
  alert("저장된 분배 비율을 가져오는 기능입니다.");
};
</script>

<style scoped>
.exchange-page-container {
  font-family: 'Pretendard', sans-serif;
  background-color: #f6f6f6;
  min-width: 1400px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
  box-sizing: border-box;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  width: 100%;
}

.page-title {
  font-size: 3rem;
  font-weight: 800;
  color: #007bff;
  letter-spacing: -2px;
}

.page-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-top: 0.5rem;
  line-height: 1.5;
}

.exchange-main-wrapper {
  width: 100%;
  max-width: 1200px;
  display: flex;
  gap: 2rem;
}

.coin-list-sidebar {
  width: 200px;
  background-color: #fff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.sidebar-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #555;
  text-align: center;
  margin-bottom: 1.5rem;
}

.main-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.exchange-card-wrapper {
  background-color: #fff;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
}

.top-sections-wrapper {
  display: flex;
  gap: 2rem;
}

.card-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #555;
}

.drop-area {
  min-height: 150px;
  background-color: #f0f0f0;
  border: 2px dashed #ccc;
  border-radius: 10px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  gap: 1.5rem;
}

.targets-drop-area {
  overflow-x: auto;
  flex-wrap: nowrap;
  justify-content: flex-start;
}

.coin-width {
  width : 100%;
}

.coin-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: grab;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  gap: 0.5rem;
  flex-shrink: 0;
  margin: 0 0.5rem;
}

.coin-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.conversion-amount-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.amount-input {
  width: 80%;
  max-width: 300px;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1.2rem;
  text-align: center;
}

.conversion-ratio-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.fetch-ratio-button {
  background-color: #fff2cc;
  border: 1px solid #ffdb4d;
  color: #333;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 2rem;
  transition: background-color 0.2s;
}

.fetch-ratio-button:hover {
  background-color: #ffe680;
}

.ratio-input-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 2rem;
  width: 100%;
}

.ratio-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.ratio-bar-container {
  position: relative;
  width: 80px;
  height: 120px;
  background-color: #f0f0f0;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: flex-end;
  padding: 5px;
}

.ratio-coin-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  opacity: 0.8;
  border-radius: 50%;
  z-index: 1;
}

.ratio-bar {
  width: 70%;
  background-color: #ff6666;
  border-radius: 6px;
  transition: height 0.3s ease-in-out;
  z-index: 0;
}

.ratio-input-group {
  display: flex;
  align-items: center;
}

.ratio-input {
  width: 50px;
  height: 35px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  text-align: center;
  font-size: 1rem;
}

.percentage-symbol {
  margin-left: 0.5rem;
  font-size: 1rem;
  color: #555;
}

.ratio-coin-symbol {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-top: 0.5rem;
}

.convert-button {
  margin-top: 20px;
  width: 150px;
  padding: 0.9rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.convert-button:hover {
  background-color: #0056b3;
}
</style>
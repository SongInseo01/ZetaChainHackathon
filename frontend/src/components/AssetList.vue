<template>
  <div
      class="asset-card"
      :class="{ 'blurry': isBlurry }"
      :style="{ top: cardTop, right: cardRight, zIndex: cardZIndex }"
      @mouseenter="isHovering = true"
      @mouseleave="isHovering = false"
      @click="bringToFront"
  >
    <div class="card-header">
      <h2 class="card-title">내 가상자산</h2>
      <button class="refresh-button" @click="fetchAssets">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="currentColor"
            class="refresh-icon"
        >
          <path
              fill-rule="evenodd"
              d="M19.95 5.05a.75.75 0 0 1 .05 1.06l-2.75 2.75a.75.75 0 0 1-1.06-1.06l1.22-1.22A8.5 8.5 0 1 0 12 20.5a8.45 8.45 0 0 0 5.46-1.97l1.39 1.39a.75.75 0 1 1-1.06 1.06l-1.39-1.39A9.95 9.95 0 1 1 20 12a.75.75 0 0 1-.05-.95ZM12 4.5A7.5 7.5 0 0 0 6.6 18.06L4.56 16.02A9 9 0 1 1 12 3a9 9 0 0 1 7.44 4.14l-1.94 1.94a.75.75 0 0 1-.05 1.06Z"
              clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>

    <ul class="asset-list">
      <li v-for="asset in assets" :key="asset.currency" class="asset-item">
        <div class="asset-info">
          <span class="asset-currency">{{ asset.currency }}</span>
          <div class="asset-values">
            <span class="asset-balance">{{ asset.amount }}</span>
            <span v-if="asset.krwValue" class="asset-krw-value">
              = ₩ {{ asset.krwValue.toLocaleString() }}
            </span>
          </div>
        </div>
      </li>
    </ul>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>자산 정보를 불러오는 중입니다...</p>
    </div>

    <div v-if="error" class="error-state">
      <p>⚠️ 자산 정보를 불러오는데 실패했습니다.</p>
    </div>

    <div class="button-group">
      <button class="action-button primary" @click="startExchange">
        교환하기
      </button>
      <button class="action-button secondary" @click="openAIHelp">
        AI에게 도움 받기
      </button>
    </div>
  </div>

  <AIChatPopup v-if="showAIHelp" :show="showAIHelp" @close="closeAIHelp" />
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import axios from 'axios';
import AIChatPopup from './AIChatPopup.vue';

const props = defineProps({
  isFront: Boolean,
  isBlurry: Boolean
});

const emit = defineEmits(['goToExchange', 'bring-to-front']);

const assets = ref([]);
const loading = ref(false);
const error = ref(false);
const showAIHelp = ref(false);
const isHovering = ref(false);
let intervalId = null;

const fetchAssets = async () => {
  loading.value = true;
  error.value = false;

  const myBalance = await axios.get(`http://127.0.0.1:8876/balance`);
  const heldCoins = myBalance.data;

  heldCoins.SOL = '2929329.111';
  heldCoins.XRP = '290.238';
  heldCoins.ADA = '102032.12';
  heldCoins.BTC = '0.2323211';
  // const balanceData = await myBalance.json()
  console.log(myBalance.data, heldCoins);

  try {
    const markets = Object.keys(heldCoins).map(coin => `KRW-${coin}`).join(',');
    const response = await fetch(`https://api.bithumb.com/v1/ticker?markets=${markets}`);

    if (!response.ok) {
      throw new Error(`API 응답 오류: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    if (data && data.length > 0) {
      assets.value = Object.keys(heldCoins).map(currency => {
        const ticker = data.find(t => t.market === `KRW-${currency}`);
        if (ticker) {
          const amount = heldCoins[`${currency}`];
          const krwValue = Math.floor(amount * ticker.trade_price);
          return { currency, amount, krwValue };
        } else {
          console.warn(`Warning: Data for ${currency} not found in API response.`);
          return { currency, amount: heldCoins[`${currency}`] || 0, krwValue: 0 };
        }
      });
    } else {
      throw new Error('API 응답에 유효한 데이터가 없습니다.');
    }
  } catch (err) {
    console.error('Failed to fetch coin prices:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const startExchange = () => {
  emit('goToExchange');
};

const openAIHelp = () => {
  showAIHelp.value = true;
};

const closeAIHelp = () => {
  showAIHelp.value = false;
};

const bringToFront = () => {
  emit('bring-to-front');
};

const cardTop = computed(() => {
  return props.isFront ? '0px' : '0px';
});

const cardRight = computed(() => {
  return props.isFront ? '0px' : '-15px';
});

const cardZIndex = computed(() => {
  return props.isFront ? 2 : 1;
});

onMounted(() => {
  fetchAssets();
  intervalId = setInterval(fetchAssets, 15000);
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>

<style scoped>
.asset-card {
  background-color: #fff;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  box-sizing: border-box;
  z-index: 2;
  transition: transform 0.3s ease-in-out, z-index 0s 0.3s;
  cursor: pointer;
}

.asset-card.blurry {
  filter: blur(5px);
  transition: filter 0.5s ease-in-out;
}

/* Rest of the styles remain the same */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 1rem;
}
.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
}
.refresh-button {
  border: none;
  background-color: transparent;
  cursor: pointer;
  color: #888;
  transition: transform 0.3s;
}
.refresh-button:hover {
  transform: rotate(180deg);
}
.refresh-icon {
  width: 24px;
  height: 24px;
}
.asset-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.asset-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #f5f5f5;
}
.asset-item:last-child {
  border-bottom: none;
}
.asset-info {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.asset-currency {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}
.asset-values {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.asset-balance {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}
.asset-krw-value {
  font-size: 0.9rem;
  color: #007bff;
  font-weight: 500;
  margin-top: 0.2rem;
}
.loading-state,
.error-state {
  text-align: center;
  margin-top: 1.5rem;
}
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top-color: #007bff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #f0f0f0;
}
.action-button {
  flex: 1;
  font-size: 1.1rem;
  font-weight: 600;
  padding: 1rem;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s;
}
.action-button.primary {
  background-color: #007bff;
  color: #fff;
}
.action-button.secondary {
  background-color: #e0e0e0;
  color: #333;
}
.action-button.primary:hover {
  background-color: #0056b3;
}
.action-button.secondary:hover {
  background-color: #c4c4c4;
}
</style>
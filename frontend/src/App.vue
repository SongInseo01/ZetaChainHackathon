<template>
  <div class="main-container">
    <header class="app-header" v-if="currentPage !== 'exchange'">
      <h1 class="header-title">ZetaSwap</h1>
      <p class="header-subtitle">가상화폐를 ZetaChain을 통해 편리하게 교환하세요.<br>여러 코인을 쉽게 변환하여, 자산의 운용 효율성을 높여 드립니다.</p>
    </header>
    <main class="app-content">
      <div class="asset-container">
        <AssetList
            v-if="currentPage === 'assets'"
            @goToExchange="goToExchange"
            :is-front="isAssetListFront"
            @bring-to-front="bringAssetListToFront"
            :is-blurry="!isAssetListFront"
        />
        <InvestmentStatusCard
            v-if="currentPage === 'assets'"
            :is-front="!isAssetListFront"
            @bring-to-front="bringInvestmentStatusToFront"
            :is-blurry="isAssetListFront"
        />
      </div>
      <ExchangePage v-if="currentPage === 'exchange'" @goToAssets="goToAssets" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AssetList from './components/AssetList.vue';
import ExchangePage from './components/ExchangePage.vue';
import InvestmentStatusCard from './components/InvestmentStatusCard.vue';

const currentPage = ref('assets');
const isAssetListFront = ref(true);

const goToExchange = () => {
  currentPage.value = 'exchange';
};

const goToAssets = () => {
  currentPage.value = 'assets';
}

const bringAssetListToFront = () => {
  isAssetListFront.value = true;
};

const bringInvestmentStatusToFront = () => {
  isAssetListFront.value = false;
};
</script>

<style scoped>
.main-container {
  font-family: 'Pretendard', sans-serif;
  background-color: #f6f6f6;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #333;
}

.app-header {
  text-align: center;
  margin-bottom: 2.5rem;
  width: 100%;
}

.header-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: #007bff;
  letter-spacing: -1.5px;
}

.header-subtitle {
  font-size: 1.1rem;
  color: #666;
  margin-top: 0.5rem;
}

.app-content {
  position: relative;
  display: flex;
  justify-content: center;
  padding: 1.5rem;
  box-sizing: border-box;
  width: 100%;
  max-width: 600px;
}

.asset-container {
  position: relative;
  width: 100%;
  padding-bottom: 1.5rem;
}
</style>
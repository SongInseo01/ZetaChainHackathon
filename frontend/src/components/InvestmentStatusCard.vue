<template>
  <div
      class="investment-status-card"
      :style="{ top: cardTop, right: cardRight, zIndex: cardZIndex, transform: cardTransform }"
      @mouseenter="isHovering = true"
      @mouseleave="isHovering = false"
      @click="bringToFront"
  >
    <h2 class="card-title">투자 현황</h2>
    <div class="status-item">
      <span>총 투자액</span>
      <strong>₩ 10,000,000</strong>
    </div>
    <div class="status-item">
      <span>총 평가액</span>
      <strong>₩ 12,500,000</strong>
    </div>
    <div class="status-item">
      <span>수익률</span>
      <strong class="profit">+25%</strong>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  isFront: Boolean
});

const emit = defineEmits(['bring-to-front']);

const isHovering = ref(false);

const cardTop = computed(() => {
  if (props.isFront) {
    return '0px';
  } else if (isHovering.value) {
    return '-10px';
  } else {
    return '-15px';
  }
});

const cardRight = computed(() => {
  return props.isFront ? '0px' : '-15px';
});

const cardZIndex = computed(() => {
  return props.isFront ? 2 : 1;
});

const cardTransform = computed(() => {
  return props.isFront ? 'scale(1)' : 'scale(1)';
});

const bringToFront = () => {
  emit('bring-to-front');
};
</script>

<style scoped>
.investment-status-card {
  background-color: #fff;
  border-radius: 20px;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  position: absolute;
  top: -15px;
  right: -15px;
  width: 100%;
  box-sizing: border-box;
  z-index: 1;
  transition: top 0.3s ease-in-out, right 0.3s ease-in-out, z-index 0s 0.3s;
  cursor: pointer;
}

.investment-status-card.blurry {
  filter: blur(5px);
  transition: filter 0.5s ease-in-out;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1.5rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.7rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.status-item:last-child {
  border-bottom: none;
}

.status-item span {
  font-size: 1rem;
  color: #666;
}

.status-item strong {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.profit {
  color: #28a745;
}
</style>
<template>
  <div class="ai-chat-popup">
    <div class="chat-header">
      <h3 class="chat-title">AI 상담사</h3>
      <button class="close-button" @click="$emit('close')">X</button>
    </div>
    <div class="chat-body">
      <div v-for="message in messages" :key="message.id" :class="['chat-message', message.sender]">
        <p>{{ message.text }}</p>
      </div>
    </div>
    <div class="chat-input-area">
      <input
          v-model="inputText"
          @keyup.enter="sendMessage"
          @keyup.up="showPreviousMessage"
          type="text"
          placeholder="메시지를 입력하세요..."
          class="chat-input"
      />
      <button @click="sendMessage" class="send-button">전송</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';

const props = defineProps({
  show: Boolean
});

const emit = defineEmits(['close']);

const messages = ref([
  { id: 1, text: '안녕하세요! ZetaSwap AI 상담사입니다. 무엇을 도와드릴까요?', sender: 'ai' }
]);
const inputText = ref('');
const messageHistory = ref([]); // 이전 대화를 저장할 배열
const historyIndex = ref(-1); // 현재 보고 있는 이전 대화의 인덱스

// 가상으로 저장할 코인 목록
const coinList = ['BTC', 'ETH', 'ETC', 'LTC', 'XRP'];

const scrollToBottom = () => {
  const chatBody = document.querySelector('.chat-body');
  if (chatBody) {
    chatBody.scrollTop = chatBody.scrollHeight;
  }
};

const sendMessage = async () => {
  const trimmedText = inputText.value.trim();
  if (!trimmedText) return;

  const userMessage = {
    id: messages.value.length + 1,
    text: trimmedText,
    sender: 'user'
  };
  messages.value.push(userMessage);

  // 사용자가 보낸 메시지를 기록에 추가
  messageHistory.value.push(trimmedText);
  // 인덱스 초기화
  historyIndex.value = -1;

  if (trimmedText.startsWith('분배')) {
    const parts = trimmedText.split(' ').filter(part => part !== '');
    const ratios = parts.slice(1).map(Number).filter(n => !isNaN(n) && n >= 0);

    if (ratios.length > 0 && ratios.length <= coinList.length) {
      const total = ratios.reduce((sum, current) => sum + current, 0);
      const isTotalTenOrHundred = total === 10 || total === 100;

      const distribution = {};
      let aiResponseText = '';

      if (isTotalTenOrHundred) {
        ratios.forEach((ratio, index) => {
          distribution[coinList[index]] = ratio;
        });
        aiResponseText = `네, 분배 비율을 ${JSON.stringify(distribution, null, 2)}로 저장했습니다.`;
      } else {
        ratios.forEach((ratio, index) => {
          const percentage = (ratio / total) * 100;
          distribution[coinList[index]] = Math.round(percentage);
        });
        aiResponseText = `총합이 10 또는 100이 아니므로, 비율을 %로 변환하여 ${JSON.stringify(distribution, null, 2)}로 저장했습니다.`;
      }

      try {
        localStorage.setItem('distributionRatio', JSON.stringify(distribution));
        messages.value.push({
          id: messages.value.length + 1,
          text: aiResponseText,
          sender: 'ai'
        });
      } catch (e) {
        messages.value.push({
          id: messages.value.length + 1,
          text: '죄송합니다. 분배 비율 저장에 실패했습니다. 다시 시도해 주세요.',
          sender: 'ai'
        });
      }
    } else {
      messages.value.push({
        id: messages.value.length + 1,
        text: `분배 비율을 숫자로 입력해 주세요. (예: 분배 50 50) ${coinList.length}개 이하로 입력 가능합니다.`,
        sender: 'ai'
      });
    }
  } else {
    const aiResponse = {
      id: messages.value.length + 1,
      text: 'ZetaChain 관련 문의는 언제든지 말씀해주세요.',
      sender: 'ai'
    };
    setTimeout(() => {
      messages.value.push(aiResponse);
      nextTick(scrollToBottom);
    }, 500);
  }

  inputText.value = '';
  nextTick(scrollToBottom);
};

// 키보드 위 방향 (↑) 키 이벤트 핸들러
const showPreviousMessage = (event) => {
  // 인덱스가 0보다 작거나 이미 모든 기록을 확인했으면 종료
  if (messageHistory.value.length === 0 || historyIndex.value === 0) return;

  // 인덱스 감소 (가장 최근 메시지부터 역순으로 탐색)
  if (historyIndex.value === -1) {
    historyIndex.value = messageHistory.value.length - 1;
  } else {
    historyIndex.value--;
  }

  // 이전 메시지를 입력창에 표시
  inputText.value = messageHistory.value[historyIndex.value];

  // 키보드 커서를 입력창 끝으로 이동
  nextTick(() => {
    event.target.selectionStart = event.target.selectionEnd = inputText.value.length;
  });
};

watch(() => props.show, (newValue) => {
  if (newValue) {
    nextTick(scrollToBottom);
  }
});
</script>

<style scoped>
/* Styles remain the same as the previous response */
.ai-chat-popup {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 350px;
  height: 500px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 1000;
  animation: slideInUp 0.5s ease-out;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.chat-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #888;
}

.chat-body {
  flex-grow: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background-color: #f7f9fc;
}

.chat-message {
  max-width: 80%;
  padding: 0.8rem 1rem;
  border-radius: 18px;
  margin-bottom: 0.8rem;
  word-wrap: break-word;
}

.chat-message.user {
  background-color: #007bff;
  color: #fff;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 4px;
}

.chat-message.ai {
  background-color: #e0e0e0;
  color: #333;
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 4px;
}

.chat-input-area {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e0e0e0;
  background-color: #fff;
}

.chat-input {
  flex-grow: 1;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  outline: none;
}

.send-button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 0.75rem 1.5rem;
  margin-left: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.2s;
}

.send-button:hover {
  background-color: #0056b3;
}

@keyframes slideInUp {
  from {
    transform: translateY(50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
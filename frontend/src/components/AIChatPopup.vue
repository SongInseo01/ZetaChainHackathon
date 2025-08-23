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
import axios from 'axios';

const props = defineProps({
  show: Boolean
});

const emit = defineEmits(['close']);

const messages = ref([
  { id: 1, text: '안녕하세요! zoos AI 상담사입니다. 무엇을 도와드릴까요?', sender: 'ai' }
]);
const inputText = ref('');
const messageHistory = ref([]); 
const historyIndex = ref(-1); 

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

  messageHistory.value.push(trimmedText);
  historyIndex.value = -1;

  try {
    // --- axios POST 요청 ---
    const response = await axios({
      method: 'post',
      url: 'http://127.0.0.1:7777/llm',
      headers: {
        'Content-Type': 'application/json'
      },
      data: {
        user_input: trimmedText
      }
    });

    const aiReason = response.data?.reason || '응답을 처리할 수 없습니다.';

    messages.value.push({
      id: messages.value.length + 1,
      text: aiReason,
      sender: 'ai'
    });

    alert("hash : " + response.data?.tx_hash);
  } catch (error) {
    messages.value.push({
      id: messages.value.length + 1,
      text: '서버와 통신 중 오류가 발생했습니다.',
      sender: 'ai'
    });
  }

  inputText.value = '';
  nextTick(scrollToBottom);
};

const showPreviousMessage = (event) => {
  if (messageHistory.value.length === 0 || historyIndex.value === 0) return;

  if (historyIndex.value === -1) {
    historyIndex.value = messageHistory.value.length - 1;
  } else {
    historyIndex.value--;
  }

  inputText.value = messageHistory.value[historyIndex.value];

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
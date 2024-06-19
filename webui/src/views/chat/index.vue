<template>
  <div class="relative columnSC chat-container">
    <div class="header">
      <div class="header-item" id="llmSelectID">
        <span style="color: #333333;">LLM Model:</span>
        <el-select
            v-model="llmModel"
            class="llm-select"
            placeholder="Select"
            size="default"
            style="width: 120px"
        >
          <el-option
              v-for="item in modelList"
              :key="item"
              :label="item"
              :value="item"
          />
        </el-select>
      </div>
<!--      <div class="header-item">-->
<!--        <span style="color: #333333;">Historical Session Rounds：</span>-->
<!--        <el-input-number v-model="historyLength" size="default" :min="1" :max="5" />-->
<!--      </div>-->
    </div>

    <div ref="messagesScrollDiv" class="messages-container">
      <chat-item v-for="(item, index) in messageList" :key="index" class="infinite-list-item" :message="item" />
    </div>

    <BottomInputContainer id="BottomInputContainerID" style="width: calc(100% - 20px)" placeholder="Ask anything" @send-click="onSendClick" />

    <el-tour
        v-model="tourOpen"
        :mask="{ color: 'rgba(0, 0, 0, .3)',
    }"
    >
      <el-tour-step target="#llmSelectID" title="Select LLM">
        <div>You can select llm.</div>
      </el-tour-step>
      <el-tour-step target="#BottomInputContainerID" title="Ask anything">
        <div>You can chat with llm.</div>
      </el-tour-step>
    </el-tour>

  </div>
</template>

<script setup lang="ts" name="Index">

import {chatReq, llmModelListModelsReq} from "@/api/knowledge";
import {ElMessage} from "element-plus";
import ChatItem from "@/components/ChatItem.vue";
import BottomInputContainer from "@/components/BottomInputContainer.vue";
import moment from "moment-mini";
import { reactive, ref } from 'vue'
import { hasChatBeenShownFirstTime, setChatFirstShowStatus } from '@/utils/tour.js'

interface Message {
  role: string;
  content: string;
  time: string;
  loading: boolean;
}

const CHAT_HISTORY_KEY = 'datachat-llmchat-history'

const router = useRouter()

const llmModel: Ref<string> = ref('')

const historyLength: Ref<number> = ref(0)

const modelList = ref<string[]>([])

const messageList: Ref<Message[]> = ref([]);

const messagesScrollDiv  = ref<HTMLElement | null>(null);

const tourOpen = ref(false)

onMounted(() => {
  nextTick(() => {
    getLlmModelListModels()
    messageList.value = getLocalHistoryMessages()
  })

  if (!hasChatBeenShownFirstTime()) {
    tourOpen.value = true
    setChatFirstShowStatus(true)
  }

});

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollDiv.value) {
      messagesScrollDiv.value.scrollTop = messagesScrollDiv.value.scrollHeight;
    }
  })
}

const getLlmModelListModels = async () => {
  llmModelListModelsReq().then(res => {
    modelList.value = res.data;
    llmModel.value = modelList.value[0]
  })
}

const addUserMessage = (content: string) => {
  const userMessage: Message = {
    role: 'user',
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: false
  }
  messageList.value.push(userMessage)
}

const addRobotMessage = (content: string) => {
  const robotMessage: Message = {
    role: 'assistant',
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: true
  }
  messageList.value.push(robotMessage)
}

const updateLastRobotMessage = (content: string) => {
  const lastMessageIndex = messageList.value.length - 1;
  const lastMessage = messageList.value[lastMessageIndex];
  const updatedMessage = {
    ...lastMessage,
    content,
    loading:false
  };
  messageList.value[lastMessageIndex] = updatedMessage;
}

const updateLastRobotMessageLoading = (loading: boolean) => {
  const lastMessage = messageList.value[messageList.value.length - 1]
  lastMessage.loading = loading
}

const getHistoryMessages = () => {
  return messageList.value
  // return messageList.value.slice(-historyLength.value).map(item => {
  //   return {
  //     role: item.role,
  //     content: item.content
  //   }
  // })
}

const saveHistoryMessagesToLocal = () => {
  localStorage.setItem(CHAT_HISTORY_KEY, JSON.stringify(messageList.value))
}

const getLocalHistoryMessages = () => {
  const historyMessages = JSON.parse(localStorage.getItem(CHAT_HISTORY_KEY) || '[]')
  return historyMessages.map((item: Message) => {
    return {
      role: item.role,
      content: item.content,
      time: item.time,
      loading: item.loading
    };
  });
}

const onSendClick = (value) => {
  if (value === '') {
    ElMessage.error('Please input something')
    return
  }
  const userInputValue = value
  const historyMessages = getHistoryMessages() || []
  addUserMessage(userInputValue)
  saveHistoryMessagesToLocal()
  addRobotMessage('')
  saveHistoryMessagesToLocal()
  scrollToBottom()
  const { isDone, fetchResult } = chatReq(userInputValue,"",llmModel.value,historyMessages,historyLength.value)
  watch([isDone, fetchResult], ([done, result]) => {
    if(done){
      updateLastRobotMessageLoading(false)
      saveHistoryMessagesToLocal()
    }
    let content = ''
    result.forEach((item) => {
      content += item.text
    })
    updateLastRobotMessage(content)
    scrollToBottom()
  }, {deep: true})
}

</script>

<style>
.llm-select .el-select__wrapper {
  background-color: transparent!important;
  box-shadow: None!important;
}
</style>


<style lang="scss" scoped>
.chat-container {
  height: calc(100vh - 40px);
  overflow: hidden;
  .header {
    width: 100%;
    border-bottom: 1px solid #eeeeee;
    display: flex;
    align-items: center;
    padding: 10px 20px;
    flex-wrap: wrap;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    grid-gap: 10px 20px;
  }
  .messages-container {
    height: calc(100vh - 160px);
    width: 100%;
    flex-shrink: 1;
    background: transparent;
    overflow-y: auto;
    padding-bottom: 20px;
  }
}
</style>

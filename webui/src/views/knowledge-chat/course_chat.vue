<template>
  <div class="relative columnSC chat-container">

    <div class="rowBC" style="width: 100%; padding: 5px; background: white">
      <div class="rowAC">
        <img src="@/assets/thudb_icon.png" style="width: 50px; height: 50px"/>
        <div class="columnSS">
          <span style="font-size: 14px; color: #333333; font-weight: bold; margin-bottom: 4px">THUDBGroup</span>
          <span style="font-size: 12px; color: #666666">清华大学计算机系数据库组</span>
        </div>
      </div>
      <div class="rowAC" style="color: #1296db; margin-right: 5px; cursor: pointer" @click="gotoThuWebsite">
       <span style="margin-right: 5px">课程主页</span>
        <svg t="1714396158417" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3775" width="15" height="15"><path
            d="M675.328 117.717333a21.333333 21.333333 0 0 1-16.341333 39.402667A382.762667 382.762667 0 0 0 512 128C299.925333 128 128 299.925333 128 512s171.925333 384 384 384 384-171.925333 384-384c0-51.114667-9.984-100.8-29.12-146.986667a21.333333 21.333333 0 0 1 39.402667-16.341333A425.429333 425.429333 0 0 1 938.666667 512c0 235.648-191.018667 426.666667-426.666667 426.666667S85.333333 747.648 85.333333 512 276.352 85.333333 512 85.333333c56.746667 0 112 11.093333 163.328 32.384z m-170.88 281.152a21.290667 21.290667 0 0 1 0.042667-30.208l82.986666-82.986666a63.850667 63.850667 0 0 1 90.432 0.021333l60.373334 60.394667a63.914667 63.914667 0 0 1 0.064 90.410666l-150.997334 150.997334a63.829333 63.829333 0 0 1-90.410666-0.042667l-30.229334-30.229333a21.269333 21.269333 0 0 1 0-30.165334 21.290667 21.290667 0 0 1 30.186667 0l30.208 30.229334a21.162667 21.162667 0 0 0 30.08 0.042666l150.997333-150.997333a21.248 21.248 0 0 0-0.042666-30.08l-60.394667-60.373333a21.184 21.184 0 0 0-30.101333-0.021334l-82.986667 82.986667a21.333333 21.333333 0 0 1-30.208 0z m15.104 226.261334a21.290667 21.290667 0 0 1-0.042667 30.208l-82.986666 82.986666a63.850667 63.850667 0 0 1-90.432-0.021333l-60.373334-60.394667a63.914667 63.914667 0 0 1-0.064-90.410666l150.997334-150.997334a63.829333 63.829333 0 0 1 90.410666 0.042667l30.229334 30.229333a21.269333 21.269333 0 0 1 0 30.165334 21.290667 21.290667 0 0 1-30.186667 0l-30.208-30.229334a21.162667 21.162667 0 0 0-30.08-0.042666l-150.997333 150.997333a21.248 21.248 0 0 0 0.042666 30.08l60.394667 60.373333a21.184 21.184 0 0 0 30.101333 0.021334l82.986667-82.986667a21.333333 21.333333 0 0 1 30.208 0z" fill="#1296db" p-id="3776"></path></svg>
      </div>
    </div>
    <div ref="messagesScrollDiv" class="messages-container">
      <knowledge-chat-item
          v-for="(item, index) in messageList" :key="index" class="infinite-list-item" :message="item"
          :is-last="index === messageList.length - 1" @ignore-message-cache="ignoreMessageCache"/>
    </div>

    <BottomInputContainer id="BottomInputContainerID" style="width: calc(100% - 20px)" placeholder="询问跟课程相关的任何问题" @send-click="onSendClick"/>

  </div>
</template>

<script setup lang="ts" name="Index">

import {knowledgeChatReq, llmModelListModelsReq} from "@/api/knowledge";
import KnowledgeChatItem from "@/components/KnowledgeChatItem.vue";
import BottomInputContainer from "@/components/BottomInputContainer.vue";
import {ElMessage} from "element-plus";
import moment from "moment-mini";
import {ref} from 'vue'

interface KnowledgeMessage {
  role: string;
  ask: string;
  content: string;
  time: string;
  loading: boolean;
  docs: string[],
  docsDetail: object[],
  cache: boolean;
  cacheData: object[]
}

const KNOWLEDGE_MOBILE_CHAT_HISTORY_KEY = 'datachat-knowledge-mobile-chat-history'
const KNOWLEDGE_CHAT_USR_CACHE_KEY = 'datachat-knowledge-chat-use-cache'

const router = useRouter()

const llmModel: Ref<string> = ref('')

const historyLength: Ref<number> = ref(0)

const useCache = ref(false);

const modelList = ref<string[]>([])

const knowledgeBase: Ref<string> = ref('db_course')

const messageList: Ref<KnowledgeMessage[]> = ref([]);

const messagesScrollDiv = ref<HTMLElement | null>(null);

const tourOpen = ref(false)

watch(useCache, (newValue) => {
  localStorage.setItem(KNOWLEDGE_CHAT_USR_CACHE_KEY, String(newValue));
});


onMounted(() => {
  nextTick(() => {
    getLlmModelListModels()
    messageList.value = getLocalHistoryMessages()
  })
});

const gotoThuWebsite = () => {
  window.open('https://dbgroup.cs.tsinghua.edu.cn/ligl/courses_cn.html', '_blank');
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollDiv.value) {
      messagesScrollDiv.value.scrollTop = messagesScrollDiv.value.scrollHeight;
    }
  })
}

const getLlmModelListModels = async () => {
  llmModelListModelsReq().then(res => {
    modelList.value = res.data || [];
    llmModel.value = modelList.value[0]
  })
}

const addUserMessage = (content: string) => {
  const userMessage: KnowledgeMessage = {
    role: 'user',
    ask: '',
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: false,
    docs: [],
    docsDetail: [],
    cache: false,
    cacheData: []
  }
  messageList.value.push(userMessage)
}

const addRobotMessage = (content: string, ask: string) => {
  const robotMessage: KnowledgeMessage = {
    role: 'assistant',
    ask,
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: true,
    docs: [],
    docsDetail: [],
    cache: false,
    cacheData: []
  }
  messageList.value.push(robotMessage)
}

const updateLastRobotMessage = (content: string, docs: string[], docsDetail: object[], cache: boolean, cacheData: object[]) => {
  const lastMessageIndex = messageList.value.length - 1;
  const lastMessage = messageList.value[lastMessageIndex];
  const updatedMessage = {
    ...lastMessage,
    content,
    docs,
    docsDetail,
    cache,
    cacheData,
    loading: false
  };
  messageList.value[lastMessageIndex] = updatedMessage;
}

const updateLastRobotMessageLoading = (loading: boolean) => {
  const lastMessage = messageList.value[messageList.value.length - 1]
  lastMessage.loading = loading
}

const getHistoryMessages = () => {
  return messageList.value
}

const saveHistoryMessagesToLocal = () => {
  localStorage.setItem(KNOWLEDGE_MOBILE_CHAT_HISTORY_KEY + knowledgeBase.value, JSON.stringify(messageList.value))
}

const ignoreMessageCache = (message: KnowledgeMessage) => {
  const userInputValue = message.ask
  updateLastRobotMessage("", [], [], false, [])
  updateLastRobotMessageLoading(true)
  saveHistoryMessagesToLocal()
  knowledgeChat(userInputValue, true, true)
}

const getLocalHistoryMessages = () => {
  const historyMessages = JSON.parse(localStorage.getItem(KNOWLEDGE_MOBILE_CHAT_HISTORY_KEY + knowledgeBase.value) || '[]')
  return historyMessages.map((item: KnowledgeMessage) => {
    return {
      role: item.role,
      ask: item.ask,
      content: item.content,
      time: item.time,
      loading: item.loading,
      docs: item.docs || [],
      docsDetail: item.docsDetail || [],
      cache: item.cache || false,
      cacheData: item.cacheData || []
    };
  });
}

const onSendClick = (value) => {
  if (value === '') {
    ElMessage.error('Please input something')
    return
  }
  const userInputValue = value
  addUserMessage(userInputValue)
  saveHistoryMessagesToLocal()
  addRobotMessage('', userInputValue)
  saveHistoryMessagesToLocal()
  scrollToBottom()
  knowledgeChat(userInputValue, !useCache.value, useCache.value)
}

const knowledgeChat = (userInputValue, ignoreCache, answerCache,) => {
  const historyMessages = getHistoryMessages() || []
  const {
    isDone,
    fetchResult
  } = knowledgeChatReq(userInputValue, ignoreCache, answerCache, knowledgeBase.value, llmModel.value, historyMessages, historyLength.value)
  watch([isDone, fetchResult], ([done, result]) => {
    let answer = ''
    let docs: any[] = [];
    let docsDetail: any[] = [];
    let cache = false
    let cacheData: any[] = [];
    try {
      if (Array.isArray(result)) {
        for (const item of result) {
          answer += (item.answer || '')
          docs = [...docs, ...(item.docs || [])]
          docsDetail = [...docsDetail, ...(item.docsDetail || [])]
          cache = item.cache || false
          cacheData = [...cacheData, ...(item.cacheData || [])]
        }
      }
    } catch (e) {
      console.log(e)
    }
    if (done) {
      updateLastRobotMessageLoading(false)
      saveHistoryMessagesToLocal()
    }
    if (!answer.includes('No Cache')) {
      updateLastRobotMessage(answer, docs || [], docsDetail || [], cache || false, cacheData || [])
    } else {
      knowledgeChat(userInputValue, true, true)
    }
    scrollToBottom()
  }, {deep: true})
}

</script>

<style>
.llm-select .el-select__wrapper {
  background-color: transparent !important;
  box-shadow: None !important;
}
</style>


<style lang="scss" scoped>
.chat-container {
  height: calc(100vh - 20px);
  overflow: hidden;

  .messages-container {
    height: 100vh;
    width: 100%;
    flex-shrink: 1;
    background: transparent;
    overflow-y: auto;
    padding-bottom: 20px;
  }
}
</style>

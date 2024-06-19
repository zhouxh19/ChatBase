<template>
  <div class="relative columnSC chat-container">
    <div class="header">
      <div id="llmSelectID" class="header-item">
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

      <div id="knowledgeSelectID" class="header-item">
        <span style="color: #333333;">Knowledge Base:</span>
        <el-select
            v-model="knowledgeBase"
            class="llm-select"
            placeholder="Select"
            size="default"
            style="width: 120px"
        >
          <el-option
              v-for="item in knowledgeBaseList"
              :key="item"
              :label="item"
              :value="item"
          />
        </el-select>
      </div>

      <!--      <div class="header-item">-->
      <!--        <span style="color: #333333;">Historical Session Rounds：</span>-->
      <!--        <el-input-number v-model="historyLength" size="default" :min="1" :max="5"/>-->
      <!--      </div>-->

      <div id="useCacheID" class="header-item">
        <span style="color: #333333;">Use Cache：</span>
        <el-switch v-model="useCache" size="default"/>
      </div>

    </div>

    <div ref="messagesScrollDiv" class="messages-container">
      <knowledge-chat-item
          v-for="(item, index) in messageList" :key="index" class="infinite-list-item" :message="item"
          :is-last="index === messageList.length - 1" @ignore-message-cache="ignoreMessageCache"/>
    </div>

    <BottomInputContainer id="BottomInputContainerID" style="width: calc(100% - 20px)" placeholder="Ask anything" @send-click="onSendClick"/>

    <el-tour
        v-model="tourOpen"
        :mask="{ color: 'rgba(0, 0, 0, .3)',
    }"
    >
      <el-tour-step target="#llmSelectID" title="Select LLM">
        <div>You can select llm.</div>
      </el-tour-step>
      <el-tour-step target="#knowledgeSelectID" title="Select Knowledge Base">
        <div>You can select the knowledge base. If it is not already created, you can create it in the knowledge base on the left navigation bar.</div>
      </el-tour-step>
      <el-tour-step target="#useCacheID" title="Use Cache">
        <div>Whether to use the cache? After the cache is used, the system caches subsequent questions and answers. If a question queried again matches a historical question, the system returns the result of the historical questions first.</div>
      </el-tour-step>
      <el-tour-step target="#BottomInputContainerID" title="Ask anything">
        <div>You can ask questions about the knowledge base.</div>
      </el-tour-step>
    </el-tour>

  </div>
</template>

<script setup lang="ts" name="Index">

import {knowledgeChatReq, knowledgeListReq, llmModelListModelsReq} from "@/api/knowledge";
import KnowledgeChatItem from "@/components/KnowledgeChatItem.vue";
import BottomInputContainer from "@/components/BottomInputContainer.vue";
import {ElMessage} from "element-plus";
import moment from "moment-mini";
import {ref} from 'vue'
import {hasKnowledgeChatBeenShownFirstTime, setKnowledgeChatFirstShowStatus} from '@/utils/tour.js'

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

const KNOWLEDGE_CHAT_HISTORY_KEY = 'datachat-knowledge-chat-history'
const KNOWLEDGE_CHAT_USR_CACHE_KEY = 'datachat-knowledge-chat-use-cache'
const KNOWLEDGE_CHAT_KNNAME_KEY = 'datachat-knowledge-chat-kb'

const router = useRouter()

const llmModel: Ref<string> = ref('')

const historyLength: Ref<number> = ref(0)

const useCache = ref(localStorage.getItem(KNOWLEDGE_CHAT_USR_CACHE_KEY) === 'true');

const modelList = ref<string[]>([])

const knowledgeBaseList = ref<string[]>([])

const knowledgeBase: Ref<string> = ref(localStorage.getItem(KNOWLEDGE_CHAT_KNNAME_KEY) || '')

const messageList: Ref<KnowledgeMessage[]> = ref([]);

const messagesScrollDiv = ref<HTMLElement | null>(null);

const tourOpen = ref(false)

watch(useCache, (newValue) => {
  localStorage.setItem(KNOWLEDGE_CHAT_USR_CACHE_KEY, String(newValue));
});

watch(knowledgeBase, (newValue) => {
  localStorage.setItem(KNOWLEDGE_CHAT_KNNAME_KEY, String(newValue));
  messageList.value = getLocalHistoryMessages()
});

onMounted(() => {
  nextTick(() => {
    getLlmModelListModels()
    getKnowledgeList()
    messageList.value = getLocalHistoryMessages()
  })
  if (!hasKnowledgeChatBeenShownFirstTime()) {
    tourOpen.value = true
    setKnowledgeChatFirstShowStatus(true)
  }
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollDiv.value) {
      messagesScrollDiv.value.scrollTop = messagesScrollDiv.value.scrollHeight;
    }
  })
}

const getKnowledgeList = async () => {
  knowledgeListReq().then(res => {
    knowledgeBaseList.value = [...new Set<string>(res.data.map(item => item.kb_name))];
    if (!knowledgeBaseList.value.includes(knowledgeBase.value)) {
      knowledgeBase.value = knowledgeBaseList.value[0]
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
  localStorage.setItem(KNOWLEDGE_CHAT_HISTORY_KEY + knowledgeBase.value, JSON.stringify(messageList.value))
}

const ignoreMessageCache = (message: KnowledgeMessage) => {
  const userInputValue = message.ask
  updateLastRobotMessage("", [], [], false, [])
  updateLastRobotMessageLoading(true)
  saveHistoryMessagesToLocal()
  knowledgeChat(userInputValue, true, true)
}

const getLocalHistoryMessages = () => {
  const historyMessages = JSON.parse(localStorage.getItem(KNOWLEDGE_CHAT_HISTORY_KEY + knowledgeBase.value) || '[]')
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
  // const historyMessages = getHistoryMessages() || []
  const historyMessages = []
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

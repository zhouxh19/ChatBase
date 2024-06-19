<template>
  <div class="relative chat-container">

    <div class="layout-flow">
      <VueFlow
style="width: 100%; height: 300px" :default-viewport="{ zoom: 0.5 }" :max-zoom="4" :min-zoom="1" :nodes="nodes" :edges="edges"
               @nodes-initialized="layoutGraph('LR')">
        <template #node-process="props">
          <el-popover
              placement="right-start"
              width="60%"
              trigger="click"
          >
            <multi-source-data-node-show :message="props.data" />
            <template #reference>
              <ProcessNode
                  :data="props.data"
                  :source-position="props.sourcePosition" :target-position="props.targetPosition" />
            </template>
          </el-popover>
        </template>

        <template #edge-animation="edgeProps">
          <AnimationEdge
              :id="edgeProps.id"
              :source="edgeProps.source"
              :target="edgeProps.target"
              :source-x="edgeProps.sourceX"
              :source-y="edgeProps.sourceY"
              :targetX="edgeProps.targetX"
              :targetY="edgeProps.targetY"
              :source-position="edgeProps.sourcePosition"
              :target-position="edgeProps.targetPosition"
          />
        </template>

        <Background style="width: 100%; height: 300px" />

        <Panel class="process-panel" position="top-right">
          <el-popover
              placement="bottom-start"
              effect="light"
              width="auto"
              trigger="hover"
          >
            <div class="rowCC" style="width: 100%;">
              <!--                  <div class="columnBC shadow add-container" style="margin-right: 10px;" @click="onAddDatabaseOptionClick">-->
              <!--                    <el-icon size="24"><Coin /></el-icon>-->
              <!--                    <span style="margin-top: 10px">添加数据库</span>-->
              <!--                  </div>-->
              <div class="columnBC shadow add-container" @click="onAddFileOptionClick">
                <el-icon size="24"><List /></el-icon>
                <span style="margin-top: 10px">添加文件</span>
              </div>

            </div>
            <template #reference>
              <el-button id="addFileOptionID" size="default" type="success" circle>
                <el-icon color="#ffffff" size="24"><Plus /></el-icon>
              </el-button>
            </template>
          </el-popover>
        </Panel>

      </VueFlow>
    </div>
    <div ref="messagesScrollDiv" class="messages-container">
      <chat-item v-for="(item, index) in messageList" :key="index" :message="item" />
    </div>
    <BottomInputContainer id="BottomInputContainerID" style="width: 100%" placeholder="请输入你的需求，例如：查看订单在所有国家的分布情况" @send-click="onSendClick" >
      <template #left>
        <div style="margin-right: 10px; cursor: pointer" @click="onPromptConfigClick">
          <svg t="1709047097752" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="12784" width="26" height="26"><path
              d="M816.832 787.712v63.488a44.8 44.8 0 0 1-89.6 0v-63.488c14.4 3.712 29.248 6.208 44.8 6.208 15.552 0 30.4-2.496 44.8-6.208zM556.8 592.832v258.304a44.8 44.8 0 1 1-89.6 0V592.768c14.4 3.648 29.248 6.144 44.8 6.144 15.552 0 30.4-2.496 44.8-6.144z m-260.032 194.88v63.488a44.8 44.8 0 0 1-89.6 0v-63.488c14.4 3.712 29.248 6.208 44.8 6.208 15.552 0 30.4-2.496 44.8-6.208z m-44.8-302.208a123.968 123.968 0 1 1 0 247.936 123.968 123.968 0 0 1 0-247.936z m520.064 0a123.968 123.968 0 1 1 0 247.936 123.968 123.968 0 0 1 0-247.936z m-520.064 89.6a34.432 34.432 0 1 0 0.064 68.864 34.432 34.432 0 0 0-0.064-68.864z m520.064 0a34.432 34.432 0 1 0 0.064 68.864 34.432 34.432 0 0 0-0.064-68.864zM512 290.56a123.968 123.968 0 1 1 0 247.936A123.968 123.968 0 0 1 512 290.56z m0 89.6a34.496 34.496 0 0 0 0 68.736 34.432 34.432 0 0 0 0-68.8zM251.968 128a44.8 44.8 0 0 1 44.8 44.8v258.432a181.44 181.44 0 0 0-44.8-6.144c-15.552 0-30.4 2.496-44.8 6.144V172.8a44.8 44.8 0 0 1 44.8-44.864z m520.064 0a44.8 44.8 0 0 1 44.8 44.8v258.432a181.44 181.44 0 0 0-44.8-6.144c-15.552 0-30.4 2.496-44.8 6.144V172.8a44.8 44.8 0 0 1 44.8-44.864zM512 128a44.8 44.8 0 0 1 44.8 44.8v63.36a181.44 181.44 0 0 0-44.8-6.08c-15.552 0-30.4 2.496-44.8 6.144V172.8A44.8 44.8 0 0 1 512 128z" fill="#1296db" p-id="12785"/></svg>
        </div>
      </template>
    </BottomInputContainer>

    <el-tour
        v-model="tourOpen"
        :mask="{ color: 'rgba(0, 0, 0, .3)',
    }"
    >
      <el-tour-step target="#addFileOptionID" title="Add Files">
        <div>You can add files to the conversation here. The dialog is based on the contents of the file: for example, view the sum of X column data in a table.</div>
      </el-tour-step>
      <el-tour-step target="#BottomInputContainerID" title="Ask anything">
        <div>Talk according to the contents of the file .</div>
      </el-tour-step>
    </el-tour>

    <el-dialog v-model="dialogEditDatabaseVisible" title="Edit Database" width="800" destroy-on-close :close-on-click-modal="false">
      <el-form ref="ruleFormRef" size="default" :model="editDatabaseForm" label-width="80">
        <el-form-item label="host" prop="host" :rules="[{required: true, message: 'Please Input host', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.host" size="default" />
        </el-form-item>
        <el-form-item label="user" prop="user" :rules="[{required: true, message: 'Please Input user', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.user" size="default" />
        </el-form-item>
        <el-form-item label="password" prop="password" :rules="[{required: true, message: 'Please Input password', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.password" size="default" show-password />
        </el-form-item>
        <el-form-item label="database" prop="database" :rules="[{required: true, message: 'Please Input database', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.database" size="default" />
        </el-form-item>
        <el-form-item label="port" prop="port" :rules="[{required: true, message: 'Please Input port', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.port" size="default" />
        </el-form-item>

        <el-form-item label="Intro" prop="intro" :rules="[{required: true, message: 'Please Input intro', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.intro" placeholder="请输入该数据库的相关介绍" type="textarea" :rows="2" size="default" />
        </el-form-item>

        <el-form-item label="Prompt" prop="prompt" :rules="[{required: true, message: 'Please Input prompt', trigger: 'blur'}]">
          <el-input v-model="editDatabaseForm.prompt" placeholder="请输入获取该数据库数据的提示词" type="textarea" :rows="2" size="default" />
        </el-form-item>

      </el-form>

      <div class="rowSC">
        <el-button plain size="default" type="primary" @click="onDatabaseDDLClick">
          <el-icon style="margin-right: 10px"><Link /></el-icon>
          Test Connection and Get DDL
        </el-button>
      </div>

      <div v-if="editDatabaseForm.ddl && editDatabaseForm.ddl.length > 0" class="rowSC wrap" style="margin-top: 20px">
        <el-tabs
            v-model="ddlActiveName"
            style="width: 100%"
        >
          <el-tab-pane v-for="(item, index) in editDatabaseForm.ddl" :key="index" :label="item.table" :name="index.toString()">
            <div>
              <el-input
                  v-model="item.ddl"
                  type="textarea"
                  :rows="10"
                  placeholder="DDL"
                  :disabled="true"
                  style="width: 100%"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <template v-if="editDatabaseForm.ddl && editDatabaseForm.ddl.length > 0" #footer>
        <div class="dialog-footer">
          <el-button type="primary" size="default" @click="onCreateDatabaseClick()">
            Save to localStorage
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogAddFileVisible" title="Add File" width="800" destroy-on-close :close-on-click-modal="false">
      <el-upload
          ref="upload"
          class="multi-source-file-upload"
          :limit="1"
          action=""
          :http-request="uploadFile"
          :auto-upload="false"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            excel/csv file only
          </div>
        </template>
      </el-upload>

      <div class="rowSC">
        <el-button plain size="default" type="primary" @click="onFileDDLClick">
          <el-icon style="margin-right: 10px"><Link /></el-icon>
          Upload
        </el-button>
      </div>

      <div v-if="editDatabaseForm.ddl && editDatabaseForm.ddl.length > 0" class="rowSC wrap" style="margin-top: 20px">
        <el-tabs
            v-model="ddlActiveName"
            style="width: 100%"
        >
          <el-tab-pane v-for="(item, index) in editDatabaseForm.ddl" :key="index" :label="item.table" :name="index.toString()">
            <div>
              <el-input
                  v-model="item.ddl"
                  type="textarea"
                  :rows="10"
                  placeholder="DDL"
                  :disabled="true"
                  style="width: 100%"
              />
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>

      <template v-if="editDatabaseForm.ddl && editDatabaseForm.ddl.length > 0" #footer>
        <div class="dialog-footer">
          <el-button type="primary" size="default" @click="onCreateDatabaseClick()">
            Save to localStorage
          </el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogPromptConfigVisible" title="Database Prompt Config" width="80%" destroy-on-close :close-on-click-modal="false">
      <el-form ref="promptFormRef" size="default" :model="promptConfigForm" label-width="150">
        <el-form-item label="Prompt" prop="prompt" :rules="[{required: true, message: 'Please Input Prompt', trigger: 'blur'}]">
          <el-input v-model="promptConfigForm.prompt" type="textarea" :autosize="{ minRows: 8, maxRows: 24 }" size="default" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" size="default" @click="onSavePromptClick()">
            Save to localStorage
          </el-button>
        </div>
      </template>
    </el-dialog>

  </div>
</template>

<script setup lang="ts" name="Index">

import {chatReq} from "@/api/knowledge";
import {dbDdlInfoReq} from "@/api/database";
import {allMultiSourceFilesReq, runCodeReq, uploadMultiSourceFileReq} from "@/api/multiSource";
import ChatItem from "@/components/ChatItem.vue";
import MultiSourceDataNodeShow from "@/components/MultiSourceDataNodeShow.vue"
import BottomInputContainer from "@/components/BottomInputContainer.vue";
import {hasMultiSourceChatBeenShownFirstTime, setMultiSourceChatFirstShowStatus} from "@/utils/tour";
import type { UploadInstance} from "element-plus";
import {ElMessage, ElMessageBox} from "element-plus";
import { Panel, VueFlow, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import ProcessNode from './ProcessNode.vue'
import AnimationEdge from './AnimationEdge.vue'
import { initialEdges } from './initial-elements.js'
import { generateNode } from './node.js'
import { useRunProcess } from '@/views/multi-source-chat/useRunProcess.js'
import { useShuffle } from '@/views/multi-source-chat/useShuffle.js'
import { useLayout } from '@/views/multi-source-chat/useLayout.js'
import { v4 as uuidv4 } from 'uuid';

import moment from "moment-mini";
import {reactive, ref} from 'vue'

interface DatabaseConfig {
  host: string,
  user: string,
  password: string,
  database: string,
  port: string,
  ddl: []
}

interface MultiSourceMessage {
  role: string;
  ask: string;
  content: string;
  time: string;
  loading: boolean;
  query: string;
  queryResult: object;
  queryChatOption: object;
}

const MULTISOURCE_CHAT_HISTORY_KEY = 'multiSource-chat-history'

const MULTISOURCE_OPTIONS_KEY = 'multiSource-data-options'

const MULTISOURCE_PROMPT_KEY = 'multiSource-prompt'

const llmModel: Ref<string> = ref('')

const historyLength: Ref<number> = ref(3)

const databaseOptionList = ref<object[]>([])

const multiSourceFiles = ref<object[]>([])

const promptFormRef = ref<FormInstance>()

const databaseSelect = reactive<DatabaseConfig>({
  host: '',
  user: '',
  password: '',
  database: '',
  port: '',
  ddl: []
})

const tourOpen = ref(false)

const ruleFormRef = ref<FormInstance>()

const dialogEditDatabaseVisible = ref(false)

const dialogPromptConfigVisible = ref(false)

const dialogAddFileVisible = ref(false)

const editDatabaseForm = reactive({
  id: '',
  type: '',
  host: '',
  user: '',
  password: '',
  database: '',
  port: '',
  file_name: '',
  ddl: []
})

const promptConfigForm = reactive({
  prompt:
    '你是一名高级数据分析专家，回答有三部分，设计理由(理由应详细且合理，100字以内)、使用到的数据源地址、Python执行代码(代码中不需要添加注释, 方法名为gen_code)，且回答必须类似于以下格式：\n<h3>\n为了找出[日本每年的销售额]，我们需要以下步骤：\n 1. 在nation数据集中找到代表日本的n_nationkey。\n 2. 在customer数据集中找到对应的c_custkey，即在哪些客户来自日本。\n 3. 利用这些c_custkey在orders数据集中找到所有的订单，并加总o_totalprice\",\n</h3>\n使用到的数据源：\n```json\n[\"./multi_source_files/tpch_nation.csv\"]\n```\n生成的代码：\n```python\ndef gen_code():\n    import pandas as pd\n    nations = pd.read_csv("./multi_source_files/tpch_nation.csv\", names=[\"n_nationkey\", \"n_name\", \"n_regionkey\", \"n_comment\"])\n    customers = pd.read_csv(\"./multi_source_files/tpch_customer.csv\",names=[\"c_custkey\", \"c_name\", \"c_address\", \"c_nationkey\", \"c_phone\", \"c_acctbal\", \"c_mktsegment\", \"c_comment\"])\n    orders = pd.read_csv(\"./multi_source_files/tpch_orders.csv\", names=[\"o_orderkey\", \"o_custkey\", \"o_orderstatus\", \"o_totalprice\", \"o_orderdate\", \"o_orderpriority\", \"o_clerk\", \"o_shippriority\", \"o_comment\"])\n    japan_key = nations[nations[\"n_name\"] == \"Japan\"][\"n_nationkey\"].values[0]\n    japan_cust_keys = customers[customers[\"c_nationkey\"] == japan_key][\"c_custkey\"].unique()\n    sales = orders[orders[\"o_custkey\"].isin(japan_cust_keys)][\"o_totalprice\"].sum()\n    return {\"column_names\": [\"Annual Sales\"], \"data\": [[sales]]}\n```\n\n你需要根据数据集信息和根据用户问题，给出能够计算出问题答案的Python3代码，该代码要求能稳定运行且执行后能得到正确的结果，return的格式需要处理成能够反序列化的Json格式，字段要求如下：{\"column_names\": [\"a\", \"b\"], \"data\": [[1, \"a\"],[2, \"b\"]]}。\n\n额外要求：1、如果某行的数值型数据为空，则该数值等于0。2、尽可能少的关联数据源、3、不允许添加编造成分。4、三方库的import放到def中。\n用户的问题是: {ask}.\n数据集信息为: {ddl}.',
})

const messageList: Ref<MultiSourceMessage[]> = ref([]);

const messagesScrollDiv = ref<HTMLElement | null>(null);

const ddlActiveName = ref('0')

const nodes: Ref<object[]> = ref([]);

const edges: Ref<object[]> = ref([]);

const cancelOnError = ref(true)

const shuffle = useShuffle()

const { graph, layout, previousDirection } = useLayout()

const upload = ref<UploadInstance>()

const { run, stop, reset, isRunning } = useRunProcess({ graph, cancelOnError })

const currentNodeMessage = reactive<MultiSourceMessage>({
  role: '',
  ask: '',
  content: '',
  time: '',
  loading: false,
  query: '',
  queryResult: {},
  queryChatOption: {}
})

onMounted(() => {
  nextTick(() => {
    // databaseOptionList.value = JSON.parse(localStorage.getItem(MULTISOURCE_OPTIONS_KEY) || '[]')
    // if (databaseOptionList.value.length > 0) {
    //   onDatabaseClick(databaseOptionList.value[0])
    // }
    const promptConfig = JSON.parse(localStorage.getItem(MULTISOURCE_PROMPT_KEY) || '{}')
    if (promptConfig.prompt) {
      promptConfigForm.prompt = promptConfig.prompt
    }
    getAllMultiSourceFiles()
    messageList.value = getLocalHistoryMessages()
    Object.assign(currentNodeMessage, getLastMessage())
  })

  if (!hasMultiSourceChatBeenShownFirstTime()) {
    tourOpen.value = true
    setMultiSourceChatFirstShowStatus(true)
  }
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesScrollDiv.value) {
      messagesScrollDiv.value.scrollTop = messagesScrollDiv.value.scrollHeight;
    }
  })
}

const onDatabaseClick = (item) => {
  if(JSON.stringify(item) === JSON.stringify(databaseSelect)) {
    return
  }
  Object.assign(databaseSelect, item)
  messageList.value = getLocalHistoryMessages()
}

const resetDataForm = (item) => {
  editDatabaseForm.id = item?.id || '';
  editDatabaseForm.type = item?.type || '';
  editDatabaseForm.file_name = item?.file_name || "";
  editDatabaseForm.host = item?.host || "";
  editDatabaseForm.user = item?.user || "";
  editDatabaseForm.password = item?.password || "";
  editDatabaseForm.database = item?.database || "";
  editDatabaseForm.port = item?.port || "";
  editDatabaseForm.ddl = item?.ddl || [];
}

const onAddDatabaseOptionClick = () => {
  resetDataForm({id: generateUuid(), type: 'db'})
  ddlActiveName.value = '0'
  dialogEditDatabaseVisible.value = true
}

const onEditDatabaseOptionClick = (item) => {
  resetDataForm(item)
  ddlActiveName.value = '0'
  dialogEditDatabaseVisible.value = true
}

const onPromptConfigClick = () => {
  dialogPromptConfigVisible.value = true
}

const savePromptToLocalStorage = () => {
  localStorage.setItem(MULTISOURCE_PROMPT_KEY, JSON.stringify(promptConfigForm))
}

const onSavePromptClick = () => {
  promptFormRef.value.validate((valid) => {
    if (valid) {
      savePromptToLocalStorage()
      dialogPromptConfigVisible.value = false
    }
  })
}

const onDatabaseDDLClick = () => {
  ruleFormRef.value.validate((valid) => {
    if (valid) {
      dbDdlInfoReq(editDatabaseForm).then(res => {
        editDatabaseForm.ddl = res.data
      })
    }
  })
}

const onAddFileOptionClick = () => {
  resetDataForm({id: generateUuid(), type: 'file'})
  ddlActiveName.value = '1'
  dialogAddFileVisible.value = true
}

const onFileDDLClick = () => {
  upload.value!.submit()
}

const uploadFile = (files) => {
  uploadMultiSourceFileReq(files.file).then(() => {
    ElMessage({
      type: 'success',
      message: 'Upload File Completed',
    })
    dialogAddFileVisible.value = false
  }).finally(() => {})
}

const saveDatabaseOptionsToLocalStorage = () => {
  localStorage.setItem(MULTISOURCE_OPTIONS_KEY, JSON.stringify(databaseOptionList.value))
}

const onDeleteDatabaseOptionClick = (item) => {

  ElMessageBox.confirm(
      'Will delete the Database. Continue?',
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
  )
      .then(() => {
        databaseOptionList.value = databaseOptionList.value.filter(i => i['host'] + i['database'] !== item.host + item.database)
        saveDatabaseOptionsToLocalStorage()
        if (databaseOptionList.value.length > 0) {
          onDatabaseClick(databaseOptionList.value[0])
        }else {
          onDatabaseClick({})
        }
      }).catch(() => {})
}

const onCreateDatabaseClick = () => {
  ruleFormRef.value.validate((valid) => {
    if (!valid) return;

    const index = databaseOptionList.value.findIndex(i => i['host']+i['database'] === editDatabaseForm.host+editDatabaseForm.database)
    if (index >= 0) {
      databaseOptionList.value[index] = editDatabaseForm
    } else {
      databaseOptionList.value.push(editDatabaseForm)
    }
    Object.assign(databaseSelect, databaseOptionList.value[0])
    saveDatabaseOptionsToLocalStorage()
    dialogEditDatabaseVisible.value = false
  })
}

const getAllMultiSourceFiles = async () => {
  allMultiSourceFilesReq().then(res => {
    const files = res.data.files || [];
    const tempEdges = res.data.edges || [];
    multiSourceFiles.value = files
    nodes.value = multiSourceFiles.value.map(file => generateNode(file['file_id'], file))
    console.log('===nodes====:', nodes.value)

    edges.value = tempEdges.map(edge => {
      return {
        ...edge,
        id: edge.source+edge.target,
        type: '',
        animated: true
      }
    })
    console.log('====edges===:', edges.value)
  })
}

const addUserMessage = (content: string) => {
  const userMessage: MultiSourceMessage = {
    role: 'user',
    ask: '',
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: false,
    query: '',
    queryResult: {},
    queryChatOption: {}
  }
  messageList.value.push(userMessage)
}

const addRobotMessage = (content: string, ask: string) => {
  const robotMessage: MultiSourceMessage = {
    role: 'assistant',
    ask,
    content,
    time: moment().format('YYYY-MM-DD HH:mm:ss'),
    loading: true,
    query: '',
    queryResult: {},
    queryChatOption: {}
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
  const lastMessageIndex = messageList.value.length - 1;
  const lastMessage = messageList.value[lastMessageIndex];
  const updatedMessage = {
    ...lastMessage,
    loading,
  };
  messageList.value[lastMessageIndex] = updatedMessage;
  lastMessage.loading = loading
}

const getHistoryMessages = () => {
  return messageList.value.slice(-historyLength.value).map(item => {
    return {
      role: item.role,
      content: item.content
    }
  })
}

const saveHistoryMessagesToLocal = () => {
  localStorage.setItem(`${MULTISOURCE_CHAT_HISTORY_KEY}`, JSON.stringify(messageList.value))
}

const getLocalHistoryMessages = () => {
  const historyMessages = JSON.parse(localStorage.getItem(`${MULTISOURCE_CHAT_HISTORY_KEY}`) || '[]')
  return historyMessages.map((item: MultiSourceMessage) => {
    return {
      role: item.role,
      ask: item.ask,
      content: item.content,
      time: item.time,
      loading: item.loading,
      query: item.query,
      queryResult: item.queryResult || {},
      queryChatOption: item.queryChatOption || {}
    };
  });
}

const getLastMessage = () => {
  const lastMessageIndex = messageList.value.length - 1;
  return messageList.value[lastMessageIndex];
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
  const prompt = promptConfigForm.prompt.replace('{ask}', userInputValue).replace('{ddl}', JSON.stringify(multiSourceFiles.value))
  const { isDone, fetchResult } = chatReq(prompt,"", 'openai-api', [], 1)
  watch([isDone, fetchResult], ([done, result]) => {
    let content = ''
    result.forEach((item) => {
      content += item.text
    })
    updateLastRobotMessage(content)
    if(done){
      const extractResult = extractParts(content)
      if(extractResult.code) {
        content += "\n<p>请等待代码执行结果。。。</p>"
        updateLastRobotMessage(content)
        runCodeReq(extractResult.code, JSON.stringify(extractResult.path)).then(res => {
          console.log(res)
          content.replace("\n<p>请等待代码执行结果。。。</p>", "")
          const resData = res.data
          if (!resData.status) {
            content += `\n<p>执行代码报错：</p>\n\n${resData.msg}\n\n`
          }else {
            content += `\n<p>执行代码成功，结果为：</p>\n\n${JSON.stringify(resData.data)}\n\n`
            getAllMultiSourceFiles()
          }
          updateLastRobotMessage(content)
          saveHistoryMessagesToLocal()
        })
      }
      updateLastRobotMessageLoading(false)
      saveHistoryMessagesToLocal()
    }
    scrollToBottom()
  }, {deep: true})
}

const extractParts = (text: string) => {
  const result: any = {};
  const pathPattern = /```json([\s\S]*?)```/m;
  const codePattern = /```python([\s\S]*?)```/m;
  const matchPath = text.match(pathPattern);
  const matchCode = text.match(codePattern);
  if(matchPath) {
    result['path'] = JSON.parse(matchPath[1].trim());
  }
  if(matchCode) {
    result['code'] = matchCode[1].trim();
  }
  return result;
}

function generateUuid(): string {
  return uuidv4();
}

async function layoutGraph(direction) {
  nodes.value = layout(nodes.value, edges.value, direction)
}

</script>

<style>
.database-select .el-select__wrapper {
  background-color: var(--el-color-primary-light-9);
  border-radius: 8px
}
</style>

<style>

.multiSource-file-upload {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100px;
  width: 100%;
  background-color: #ffffff;
  border-radius: 8px;
  cursor: pointer;
  border: 1px dashed var(--el-color-primary);
  margin-bottom: 20px;
}
.layout-flow {
  position: relative;
  background-color: #1a192b;
  height: 300px;
  width: 100%;
  border-radius: 8px;
  margin-bottom: 10px;
}

.process-panel {
  background-color: #2d3748;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: row;
  align-items: center;
  margin-top: 10px;
}

.add-container {
  border-radius: 8px;
  padding: 10px;
  cursor: pointer;
  color: var(--el-color-primary);
  border: 1px solid var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}

.add-container:hover {
  background: var(--el-color-primary);
  color: white;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

<style lang="scss" scoped>
.chat-container {
  height: calc(100vh - 40px);
  overflow: hidden;
  padding: 20px;

  .sidebar {
    width: 180px;
    border-right: 1px solid #eeeeee;
    display: flex;
    height: 100vh;
    padding: 10px 20px;
  }

  .messages-container {
    height: calc(100vh - 440px);
    width: 100%;
    flex-shrink: 1;
    background: transparent;
    overflow-y: auto;
    overflow-x: hidden;
    padding-bottom: 20px;
  }

  .database-select-item {
    width: 100%;
    margin-bottom: 10px;
    padding: 10px 10px;
    border-radius: 10px;
    cursor: pointer;
    border: 1px solid var(--el-color-primary);
    background: var(--el-color-primary-light-9);
    .el-text {
      color: var(--el-color-primary)!important;
    }
    .el-icon {
      margin-right: 10px;
    }

    &:hover {
      background: var(--el-color-primary);
      .el-text {
        color: white!important;;
      }
    }

    &.active {
      background: var(--el-color-primary);
      .el-text {
        color: white!important;;
      }
    }
  }
}
</style>

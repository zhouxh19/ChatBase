<template>
  <div style="height: calc(100vh - 30px)">
    <el-container style="height: 100%">
      <el-aside width="200px" style="border-right: 1px solid var(--border-color); height: 100%;">
        <div class="columnSS" style="width: 100%; padding: 10px;">
          <div class="rowSC">
            <el-button icon="ArrowLeftBold" type="primary" plain circle size="large" @click="routerBack()"/>
            <div class="columnSS" style="margin-left: 10px; width: 100%">
              <span style="font-weight: bold; font-size: 22px; margin-bottom: 5px">{{ $route.query.kb_name }}</span>
              <span style="font-size: 12px; color: #666666">Data Count: {{ dataCount }}</span>
            </div>
          </div>
          <div class="columnSS" style="width: 100%; margin-top: 20px">
            <div
                :class="`rowSC menu-item ${activeIndex === 'dataset' ? ' active' : ''}`"
                @click="onMenuClick('dataset')">
              <el-icon>
                <Document/>
              </el-icon>
              <span>数据集</span>
            </div>
            <div :class="`rowSC menu-item ${activeIndex === 'search' ? ' active' : ''}`" @click="onMenuClick('search')">
              <el-icon>
                <Search/>
              </el-icon>
              <span>搜索测试</span>
            </div>
            <div
                :class="`rowSC menu-item ${activeIndex === 'setting' ? ' active' : ''}`"
                @click="onMenuClick('setting')">
              <el-icon>
                <Setting/>
              </el-icon>
              <span>配置</span>
            </div>
          </div>
        </div>
      </el-aside>
      <el-main>
        <div v-if="activeIndex === 'dataset'" class="columnAE">
          <div v-if="basicStore.isAdmin" class="rowBC" style="width: 100%">
            <el-popover placement="bottom-start" width="calc(100% - 400px)" trigger="click">
              <template #reference>
                <div v-if="taskData.value && taskData.value.length > 0" style="color: #333333; cursor: pointer">
                  当前有
                  <span style="font-size: 14px; color: var(--el-color-primary); padding-bottom: 2px; border-bottom: 1px solid var(--el-color-primary);">
                    {{ taskData.value.length }}个
                  </span>
                  任务在执行
                </div>
                <div v-else />
              </template>
              <el-table id="taskTable" key="1" :data="taskData.value" style="width: 100%;">
                <el-table-column width="300" property="id" label="id"/>
                <el-table-column width="120" property="time_start" label="Start At"/>
                <el-table-column label="files">
                  <template #default="scope">
                    <span v-if="scope.row.args">{{scope.row.args[0]}}</span>
                  </template>
                </el-table-column>
              </el-table>
            </el-popover>
            <div class="upload-container" @click="onOpenUpdateDialog">
              <span>添加新文件</span>
            </div>
          </div>
          <el-table
              id="fileTable" key="2"
              :data="fileList.value"
              style="width: 100%; border-radius: 10px;"
              :height="basicStore.isAdmin ? 'calc(100vh - 160px)' :'calc(100vh - 120px)'">
            <el-table-column prop="file_name" label="File Name" align="center"/>
            <el-table-column prop="docs_count" label="Data Count" width="120" align="center"/>
            <el-table-column fixed="right" label="Operations" width="170" align="center">
              <template #default="scope">
                <el-button text type="primary" size="small" @click="onHandleFileReviewClick(scope.row)">Review
                </el-button>
                <el-button v-if="basicStore.isAdmin" text type="primary" size="small" @click="onHandleFileDeleteClick(scope.row)">Delete
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
              v-model:current-page="currentPage"
              style="margin-top: 10px; width: 100%"
              :page-size="pageSize"
              :default-current-page="1"
              :small="true"
              :background="true"
              layout="prev, pager, next, total"
              :total="totalCount"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
          />

        </div>
        <div v-if="activeIndex === 'search'">
          <div class="rowBC" style="margin-bottom: 20px">
            <el-input
                v-model="searchValue" :rows="2" type="textarea" placeholder="Search"
                style="width: calc(100% - 100px)" @keyup.enter="onSearchClick"/>
            <el-button size="default" :disabled="searchValue.value" type="primary" @click="onSearchClick">Search
            </el-button>
          </div>
          <el-table :data="searchResult.value" style="width: 100%; border-radius: 10px;" height="calc(100vh - 140px)">
            <el-table-column prop="page_content" label="检索文档"/>
            <el-table-column prop="vs_type" label="向量库类型" width="80" align="center"/>
            <el-table-column type="expand">
              <template #default="scope">
                <div style="padding: 20px 10px; background: var(--el-color-primary-light-9);">
                  <el-descriptions title="" border :column="2" direction="vertical">
                    <el-descriptions-item class-name="my-descriptions-item" label="向量库类型" :span="1">
                      {{ scope.row.vs_type }}
                    </el-descriptions-item>
                    <el-descriptions-item class-name="my-descriptions-item" label="文件来源" :span="1">
                      {{ scope.row.metadata.source }}
                    </el-descriptions-item>
                    <el-descriptions-item class-name="my-descriptions-item" label="检索文档" :span="2">
                      {{ scope.row.page_content }}
                    </el-descriptions-item>
                    <el-descriptions-item class-name="my-descriptions-item" label="知识文档" :span="2">
                      {{ scope.row.metadata.llm_content || scope.row.page_content }}
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-if="activeIndex === 'setting'">
          <div class="relative columnSS">
            <div
                class="columnSS"
                style="padding: 20px; border-radius: 10px; margin-top: 20px; width: calc(100% - 10px)">
              <div class="rowSC" style="width: 100%;">
                <span
                    style="color: #000000; width: 180px; text-align: left; font-size: 16px; flex-shrink: 0">Name</span>
                <span style="color: #333333;">{{ editForm.kb_name }}</span>
              </div>

              <div class="rowSC" style="width: 100%; margin-top: 20px;">
                <span style="color: #000000; width: 180px; text-align: left; font-size: 16px; flex-shrink: 0">Brief Introduction</span>
                <el-input v-model="editForm.kb_info" disabled :rows="2" type="textarea"/>
              </div>

              <div class="rowSC" style="width: 100%; margin-top: 20px;">
                <span style="color: #000000; width: 180px; text-align: left; font-size: 16px; flex-shrink: 0">Embedding Model</span>
                <span style="color: #333333;">{{ editForm.embed_model }}</span>
              </div>
            </div>

            <div v-if="basicStore.isAdmin" class="rowSC" style="margin-left: 20px; margin-top: 20px">
              <el-button size="default" type="primary" @click="onHandleSaveClick">Save</el-button>
              <el-button style="margin-left: 10px" :icon="Delete" size="small" circle @click="onHandleDeleteClick"/>
            </div>

          </div>
        </div>
      </el-main>
    </el-container>
    <el-drawer
        v-model="reviewDrawer"
        :title="reviewDrawerTitle"
        class="dataset-detail-drawer"
        direction="rtl"
        size="calc(100% - 300px)"
        :append-to-body="true"
    >
      <ul v-loading="reviewDrawerLoading" class="infinite-list columnSS" style="width: 100%">
        <li
            v-for="(item, index) in fileSplitContents.value" :key="index" class="infinite-list-item"
            style="width: calc(100% - 20px)">
          <div class="columnSS" style="width: 100%;">
            <div class="rowBC infinite-list-item-header">
              <div style="color: var(--el-color-primary);">#{{ index + 1 }}</div>
              <div class="rowSC" style="color: #666666; margin-left: 10px">
                <div style="margin-right: 10px">检索文档</div>
                <svg
                    t="1708530334824" class="icon" viewBox="0 0 1024 1024" version="1.1"
                    xmlns="http://www.w3.org/2000/svg" p-id="15983" width="16" height="16">
                  <path
                      d="M854.013267 0.001792A170.751402 170.751402 0 0 1 1023.996672 170.753194v682.493612A170.751402 170.751402 0 0 1 854.013267 1023.998208H171.263657A170.495403 170.495403 0 0 1 0.000256 853.246806V170.753194A170.495403 170.495403 0 0 1 171.263657 0.001792zM363.006985 835.070869a15.615945 15.615945 0 0 0-15.615945 15.615946v13.823951a15.359946 15.359946 0 0 0 4.863983 11.263961 14.847948 14.847948 0 0 0 11.51996 4.351985l82.68771-3.839987c27.903902 0 51.199821-1.535995 68.095762-1.535995 25.59991 0 70.143754 1.535995 136.959521 4.607984h22.015923a15.615945 15.615945 0 0 0 15.615945-15.615945v-14.079951a15.615945 15.615945 0 0 0-15.615945-15.615945h-2.303992a143.103499 143.103499 0 0 1-45.82384-5.63198 42.495851 42.495851 0 0 1-24.063916-18.431936 127.999552 127.999552 0 0 1-9.727966-40.191859C588.798195 752.639158 588.798195 721.407267 588.798195 676.351425v-95.487666c0-46.591837 0-108.031622 2.559991-329.214848a15.615945 15.615945 0 0 1 15.615946-15.615945h74.23974c51.199821 0 87.039695 7.167975 104.703633 21.759924a153.599462 153.599462 0 0 1 31.48789 70.399753 15.871944 15.871944 0 0 0 17.663938 11.263961l16.895941-2.559991a15.615945 15.615945 0 0 0 13.055954-17.407939 1800.953697 1800.953697 0 0 1-7.935972-75.007738 981.500565 981.500565 0 0 1-3.327988-82.431711 12.543956 12.543956 0 0 0-4.863983-8.447971 12.287957 12.287957 0 0 0-10.495963-2.559991 236.799171 236.799171 0 0 1-39.167863 6.143979c-25.59991 2.047993-68.351761 2.81599-131.071542 2.81599h-307.198924c-55.807805 0-95.487666 0-119.039584-2.81599a278.527025 278.527025 0 0 1-36.863871-5.375981 15.103947 15.103947 0 0 0-12.799955 2.81599 16.639942 16.639942 0 0 0-6.143978 11.519959c-2.047993 31.231891-4.351985 55.551806-6.655977 72.703746s-7.423974 45.311841-14.847948 81.407715a15.871944 15.871944 0 0 0 14.591949 17.663938l18.687934 3.839987a15.615945 15.615945 0 0 0 18.175937-10.495963 161.535435 161.535435 0 0 1 35.327876-72.703746c19.711931-15.103947 56.319803-22.527921 109.823616-22.527921h71.935748a15.871944 15.871944 0 0 1 11.007961 4.607984 15.359946 15.359946 0 0 1 4.607984 11.007961v276.223033c0 99.327652 0 167.423414-2.047993 204.799284a291.838979 291.838979 0 0 1-7.167974 69.375757 45.311841 45.311841 0 0 1-23.295919 25.59991 126.463557 126.463557 0 0 1-51.199821 7.423974z m0 0"
                      fill="#13227a" p-id="15984"/>
                </svg>
                <span style="margin-left: 5px">{{ (item.page_content || item).length }}</span>
              </div>
            </div>
            <div class="infinite-list-item-content columnAS" style="width: 100%">
              <div class="rowBC" style="width: 100%">
                <div>
                  {{ item.page_content || item }}
                </div>
                <div style="cursor: pointer; font-size: 20px" @click="onHandleDetailContentClick(index)">
                  <el-icon v-if="showDetailIndex === index">
                    <ArrowUpBold/>
                  </el-icon>
                  <el-icon v-else>
                    <ArrowDownBold/>
                  </el-icon>
                </div>
              </div>
              <div v-if="showDetailIndex === index" class="detail-content">
                <span style="margin-bottom: 10px">检索文档对应的知识: </span><br/>{{
                  (item.metadata.llm_content || item.page_content) || item
                }}
              </div>
            </div>
          </div>
        </li>
      </ul>
    </el-drawer>
    <el-dialog
        v-model="updateDialogVisible"
        title=""
        width="calc(100% - 300px)"
    >
      <el-upload
          ref="upload"
          v-model:file-list="uploadFileList"
          class="upload"
          action=""
          multiple
          :on-change="handleFileChange"
          :before-remove="handleFileRemove"
          :on-exceed="handleExceed"
          :auto-upload="false"
      >
        <template #trigger>
          <el-button size="default" type="primary">Select File</el-button>
        </template>
        <template #tip>
          <div class="el-upload__tip">
            New file will cover the old file, Only HTML, MD, JSON, JSONL, CSV, PDF, PNG, JPG, JPEG,
            BMP, EML, MSG, EPUB, XLSX, XLSD, IPYNB,
            ODT, PY, RST, RTF, SRT, TOML, TSV, DOCX, DOC, XML, PPT, PPTX, TXT
          </div>
        </template>
      </el-upload>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="updateDialogVisible = false">Cancel</el-button>
          <el-button :disabled="uploadFileList.length === 0" size="default" type="success" @click="onUploadDocsClick">
            UPLOAD
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="KnowledgeDetail">
import {
  docSplitDetailsReq,
  knowledgeBaseDeleteReq,
  knowledgeBaseDetailReq,
  knowledgeBaseUpdateInfoReq,
  knowledgeDeleteDocsReq,
  knowledgeFileDetailCountReq,
  knowledgeFileDetailsReq,
  knowledgeSearchDocsReq,
  knowledgeUploadDocsReq,
  uploadActiveTasksReq
} from "@/api/knowledge";

import {useBasicStore} from "@/store/basic";

// 获取store和router
import {Delete, Document, Search, Setting} from "@element-plus/icons-vue";
import type {UploadInstance, UploadProps, UploadRawFile} from 'element-plus'
import {ElMessage, ElMessageBox, genFileId} from 'element-plus'
import {reactive, ref} from 'vue'

const basicStore = useBasicStore()

const router = useRouter()

const route = useRoute()

const activeIndex: Ref<string> = ref('dataset')

const fileList: Ref<Array<object>> = reactive([])

const currentPage = ref(1)

const pageSize = ref(20)

const totalCount = ref(0)

const dataCount = ref(0)

const showDetailIndex = ref(-1)

const reviewDrawer: Ref<boolean> = ref(false)

const reviewDrawerLoading: Ref<boolean> = ref(true)

const reviewDrawerTitle: Ref<string> = ref('')

const fileSplitContents: Ref<Array<string>> = reactive([])

const upload = ref<UploadInstance>()

const searchValue: Ref<string> = ref('')

const searchResult: Ref<Array<object>> = reactive([])

const taskData: Ref<Array<object>> = reactive([])

const updateDialogVisible: Ref<boolean> = ref(false)

const pollingTimer = ref<ReturnType<typeof setInterval> | null>(null);

const uploadFileList = ref<UploadUserFile[]>([])


const editForm = reactive({
  kb_name: '',
  kb_info: '',
  embed_model: ''
})


watch(() => activeIndex.value,
    (newValue, oldValue) => {
      console.log('activeIndex', newValue, oldValue)
      if (newValue === 'setting') {
        getKnowledgeBaseDetail()
      }
    },
    {immediate: true}
)

watch(() => taskData.value, (newValue, oldValue) => {
      if (newValue && newValue) {
        if (newValue?.length !== oldValue?.length) {
          getFileDetail()
        }
      }
    },
    {deep: true}
)


onMounted(async () => {
  activeIndex.value = route.query.activeIndex || 'dataset'
  getFileDetail()
  getDataCount()
  getUploadActiveTasks()
})

onUnmounted(() => {
  stopPolling(); // 组件卸载时停止轮询
});

const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}

const handleSizeChange = (val: number) => {
  getFileDetail()
}
const handleCurrentChange = (val: number) => {
  getFileDetail()
}

const getFileDetail = () => {
  fileList.value = []
  knowledgeFileDetailsReq(route.query.kb_name, currentPage.value, pageSize.value).then(res => {
    totalCount.value = res.data.total_count
    fileList.value = res.data.data.map(item => {
      let fileName = item.file_name;
      fileName = fileName.slice(Math.max(0, fileName.lastIndexOf('/') + 1));
      return {...item, file_name: fileName, file_path: item.file_name}
    });
  })
}

const onOpenUpdateDialog = () => {
  uploadFileList.value = []
  updateDialogVisible.value = true
  nextTick(() => {
    upload.value!.clearFiles()
  })
}

const getUploadActiveTasks = () => {
  uploadActiveTasksReq(route.query.kb_name).then(res => {
    taskData.value = res.data || []
    if (taskData.value.length > 0) {
      startPolling(); // 有任务则开始轮询
    } else {
      stopPolling(); // 没有任务则停止轮询
    }
  })
}

// 开始轮询
const startPolling = () => {
  // 首先清除已存在的定时器
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value);
  }

  // 设置定时器每隔两秒执行一次getUploadActiveTasks
  pollingTimer.value = setInterval(() => {
    getUploadActiveTasks();
  }, 5000);
};

// 停止轮询
const stopPolling = () => {
  if (pollingTimer.value) {
    clearInterval(pollingTimer.value);
    pollingTimer.value = null;
  }
};


const getDataCount = () => {
  fileList.value = []
  knowledgeFileDetailCountReq(route.query.kb_name, currentPage.value, pageSize.value).then(res => {
    dataCount.value = res.data.count
  })
}


const getKnowledgeBaseDetail = () => {
  fileList.value = []
  knowledgeBaseDetailReq(route.query.kb_name).then(res => {
    editForm.kb_name = res.data.kb_name
    editForm.kb_info = res.data.kb_info
    editForm.embed_model = res.data.embed_model
  })
}


const getFileSplitContent = (fileName) => {
  docSplitDetailsReq(route.query.kb_name, fileName).then(res => {
    fileSplitContents.value = res.data['contents'] || []
  }).finally(() => {
    reviewDrawerLoading.value = false
  })
}

const onHandleDetailContentClick = (index) => {
  if (showDetailIndex.value === index) {
    showDetailIndex.value = -1
  } else {
    showDetailIndex.value = index
  }
}

const deleteDocs = (fileName) => {
  knowledgeDeleteDocsReq(route.query.kb_name, fileName).then(() => {
    ElMessage({
      type: 'success',
      message: 'Delete completed',
    })
    getFileDetail()
  }).finally(() => {

  })
}

const onHandleSaveClick = () => {
  knowledgeBaseUpdateInfoReq(route.query.kb_name, editForm.kb_info).then(() => {
    ElMessage({
      type: 'success',
      message: 'Update completed',
    })
  })
}

const onSearchClick = () => {
  if (!searchValue.value) {
    return
  }
  searchResult.value = []
  knowledgeSearchDocsReq(route.query.kb_name, searchValue.value).then(res => {
    searchResult.value = res.data
  })
}

const onHandleDeleteClick = () => {
  ElMessageBox.confirm(
      'Will delete the Knowledge Base. Continue?',
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
  )
      .then(() => {
        knowledgeBaseDeleteReq(route.query.kb_name).then(() => {
          ElMessage({
            type: 'success',
            message: 'Delete completed',
          })
          routerBack()
        })
      }).catch(() => {
  })
}

const onUploadDocsClick = () => {
  const tempFileList: File[] = [];
  uploadFileList.value.forEach(file => {
    tempFileList.push(file.raw);
  });
  knowledgeUploadDocsReq(route.query.kb_name, tempFileList).then(() => {
    ElMessage({
      type: 'success',
      message: 'The task has been added. Wait until the task is complete',
    })
    updateDialogVisible.value = false
    getUploadActiveTasks()
  }).finally(() => {

  })
}

const handleFileChange = (file, fileList) => {
  uploadFileList.value = fileList
}

const handleFileRemove = (file, fileList) => {
  uploadFileList.value = fileList
}

const onMenuClick = (index) => {
  activeIndex.value = index
}

const onHandleFileReviewClick = (file) => {
  console.log('file:', file)
  fileSplitContents.value = []
  reviewDrawerTitle.value = file.file_name
  reviewDrawer.value = true
  reviewDrawerLoading.value = true
  getFileSplitContent(file.file_name)
}

const onHandleFileDeleteClick = (file) => {
  console.log('file:', file)
  ElMessageBox.confirm(
      'Will permanently delete the file. Continue?',
      'Warning',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }
  )
      .then(() => {
        deleteDocs(file.file_path)
      }).catch(() => {
  })
}

const routerBack = () => {
  router.back()
}

</script>

<style>
.dataset-detail-drawer {
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

.dataset-detail-drawer > .el-drawer__header {
  margin-bottom: 0 !important;
}

.upload-container {
  padding: 10px 20px;
  text-align: center;
  cursor: pointer;
  border: 1px solid var(--el-color-primary);
  background: var(--el-color-primary);
  color: white;
  border-radius: 10px;
  margin-bottom: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.upload {
  width: calc(100% - 120px);
}

.el-descriptions__body {
  background-color: transparent !important;
}
</style>

<style scoped lang="scss">

:deep(.my-descriptions-item) {
  color: #0d5aa7;
}

.menu-item {
  width: 100%;
  margin-bottom: 10px;
  padding: 10px 10px;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid var(--el-color-primary);
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);

  .el-icon {
    margin-right: 10px;
  }

  &:hover {
    background: var(--el-color-primary);
    color: white;
  }

  &.active {
    background: var(--el-color-primary);
    color: white;
  }
}

.infinite-list {
  height: 100%;
  padding: 0;
  margin: 0;
  list-style: none;
  overflow: auto;

  .infinite-list-item {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 10px;

    .infinite-list-item-header {
      margin-bottom: 10px;
      width: 100%;
    }

    .infinite-list-item-content {
      white-space: pre-wrap;
      color: var(--el-color-primary);
      background: var(--el-color-primary-light-9);
      border-radius: 4px;
      padding: 10px;
      height: auto;
    }

    .detail-content {
      white-space: pre-wrap;
      background: white;
      padding: 2px 10px;
      border-radius: 4px;
      color: #666666;
      margin-top: 10px;
      text-align: left;
    }
  }
}

</style>

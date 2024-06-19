<template>
  <div class="chat-item-container">
    <div :class="'rowSC ' + roleClass">
      <img v-if="isUser" src="@/assets/chat-user.png" class="face"/>
      <img v-else src="@/assets/chat-robot.png" class="face"/>
      <!--      <span style="margin: 0 10px; color: red">abc</span>-->
      <!--      <span style="color: #2c59cb">sdada</span>-->
      <el-button v-if="isLast && message.cache" size="small" type="primary" plain
                 style="margin-left: 10px; margin-top: 4px" @click="onIgnoreMessageCacheClick">
        <el-icon style="margin-right: 6px" size="16">
          <MostlyCloudy/>
        </el-icon>
        缓存有误，点击重新生成
      </el-button>
    </div>
    <div :class="'rowSC ' + roleClass">
      <div v-if="!message.loading">
        <div class="columnSS content">
          <template v-if="!message.cache">
            <div v-html="htmlContent"/>
            <div v-if="message.docsDetail.length > 0" class="rowSC" style="width: 100%; margin-bottom: 10px">
              <div class="rowSC" style="color: #888888; font-weight: bold; margin-right: 10px">
                <img src="@/assets/knowledge_ chat_quote.png" style="width: 20px; margin-right: 10px"/>
                引用
              </div>
              <div style="height: 1.5px; flex: 1 1 0; background: #eeeeee"/>
            </div>
            <div v-for="(item, index) in message.docsDetail" :key="index" class="rowSC quote-item"
                 @click="onQuoteClick(item)">
              <el-icon style="margin-left: 6px; margin-right: 6px" size="12" color="#06a411">
                <Document/>
              </el-icon>
              <div
                  style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; font-size: 12px!important;">
                {{ item.filename }}
                <el-tag size="small" style="margin-left: 5px; font-size: 11px!important;">{{ item.contents.length }}
                  paragraphs
                </el-tag>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="columnSS">
              <div class="rowSC"
                   style="margin: 10px 0; color: var(--el-color-success); font-size: 14px; font-weight: bold">
                <el-icon size="18" style="margin-right: 6px;">
                  <Clock/>
                </el-icon>
                历史答案的缓存命中：
              </div>
              <div v-for="(item, index) in message.cacheData" :key="index" class="columnSS"
                   style="width: 100%; margin-bottom: 10px">
                <div style="color: var(--el-color-primary); line-height: 1.2; margin-bottom: 10px">
                  ASK：{{ item.page_content }}
                </div>
                <span style="color: #666666; line-height: 1.4; white-space: pre-line;">Answer：{{ item.answer }}</span>
              </div>
            </div>
          </template>
        </div>
      </div>
      <div v-else>
        <div class="content rowBC" style="padding: 10px 20px">
          <el-icon class="is-loading" size="20" color="#333333">
            <Loading/>
          </el-icon>
        </div>
      </div>
    </div>
    <el-dialog v-model="quoteDialogVisible" class="quote-dialog" :show-close="true" width="80%" top="3vh">
      <template #header>
        <div class="quote-dialog-header">
          <el-tooltip
              class="box-item"
              effect="dark"
              content="Click to download"
              placement="bottom-start"
          >
            <div @click="navigateTo(currentQuoteItem.url)">{{ currentQuoteItem.filename }}</div>
          </el-tooltip>
        </div>
      </template>
      <div class="columnSS" style="width: 100%; max-height: calc(100vh - 16vh); overflow-y: scroll">
        <div v-for="(item, index) in currentQuoteItem.contents" :key="index" class="columnSS quote-dialog-content-item">
          <div class="rowBC wrap" style="font-size: 14px; margin-bottom: 8px; width: 100%">
            <div class="rowSC">
              <span style="margin-right: 10px; border: 1px solid #06a411; border-radius: 6px; padding: 2px 5px">#{{ index + 1 }}</span>
              <div class="rowBE" v-if="item.metadata?.media_url" style="cursor: pointer; border-bottom: 2px solid #7162AD; padding-bottom: 2px;
              padding-right: 10px" @click="navigateTo(item.metadata.media_url)">
                <svg t="1714048186871" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3169" width="20" height="20"><path
                    d="M499.2 951.466667c-234.666667 0-426.666667-192-426.666667-426.666667 0-17.066667 0-38.4 4.266667-55.466667 4.266667-12.8 12.8-17.066667 25.6-17.066666 12.8 4.266667 17.066667 12.8 17.066667 25.6-4.266667 12.8-4.266667 29.866667-4.266667 46.933333 0 213.333333 170.666667 384 384 384s384-170.666667 384-384-170.666667-384-384-384c-25.6 0-46.933333 4.266667-72.533333 8.533333-12.8 0-21.333333-4.266667-25.6-17.066666 0-12.8 4.266667-21.333333 17.066666-25.6 25.6-4.266667 51.2-8.533333 81.066667-8.533334 234.666667 0 426.666667 192 426.666667 426.666667s-192 426.666667-426.666667 426.666667z" fill="#7162AD" p-id="3170"></path><path d="M119.466667 418.133333h-8.533334c-8.533333-4.266667-17.066667-17.066667-12.8-29.866666 42.666667-119.466667 128-213.333333 238.933334-256 12.8-4.266667 21.333333 0 25.6 12.8 4.266667 12.8 0 21.333333-12.8 25.6C256 213.333333 174.933333 298.666667 140.8 405.333333c-4.266667 8.533333-12.8 12.8-21.333333 12.8z" fill="#A495FC" p-id="3171"></path><path d="M494.933333 260.266667c34.133333 0 64 29.866667 64 64s-29.866667 64-64 64-64-29.866667-64-64 29.866667-64 64-64m0-42.666667c-59.733333 0-106.666667 46.933333-106.666666 106.666667s46.933333 106.666667 106.666666 106.666666 106.666667-46.933333 106.666667-106.666666-46.933333-106.666667-106.666667-106.666667zM503.466667 665.6c34.133333 0 64 29.866667 64 64s-29.866667 64-64 64-64-29.866667-64-64 25.6-64 64-64m0-42.666667c-59.733333 0-106.666667 46.933333-106.666667 106.666667s46.933333 106.666667 106.666667 106.666667 106.666667-46.933333 106.666666-106.666667-46.933333-106.666667-106.666666-106.666667zM298.666667 465.066667c34.133333 0 64 29.866667 64 64s-29.866667 64-64 64-64-29.866667-64-64 25.6-64 64-64m0-42.666667c-59.733333 0-106.666667 46.933333-106.666667 106.666667s46.933333 106.666667 106.666667 106.666666 106.666667-46.933333 106.666666-106.666666S354.133333 422.4 298.666667 422.4zM704 460.8c34.133333 0 64 29.866667 64 64s-29.866667 64-64 64-64-29.866667-64-64 25.6-64 64-64m0-42.666667c-59.733333 0-106.666667 46.933333-106.666667 106.666667s46.933333 106.666667 106.666667 106.666667 106.666667-46.933333 106.666667-106.666667-51.2-106.666667-106.666667-106.666667zM499.2 507.733333c12.8 0 21.333333 8.533333 21.333333 21.333334s-8.533333 21.333333-21.333333 21.333333-21.333333-8.533333-21.333333-21.333333 8.533333-21.333333 21.333333-21.333334m0-42.666666c-34.133333 0-64 29.866667-64 64s29.866667 64 64 64 64-29.866667 64-64-29.866667-64-64-64z" fill="#7162AD" p-id="3172"></path><path d="M900.266667 951.466667h-426.666667c-12.8 0-21.333333-8.533333-21.333333-21.333334s8.533333-21.333333 21.333333-21.333333h426.666667c12.8 0 21.333333 8.533333 21.333333 21.333333s-8.533333 21.333333-21.333333 21.333334z" fill="#7162AD" p-id="3173"></path></svg>
                <span style="margin-left: 5px">视频</span>
              </div>
            </div>

            <div style="color: #333333" class="rowAC">
              <div style="margin-right: 10px">检索文档</div>
              <svg
                t="1708530334824" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
                p-id="15983" width="14"
                height="14">
              <path
                  fill="#333333"
                  d="M854.013267 0.001792A170.751402 170.751402 0 0 1 1023.996672 170.753194v682.493612A170.751402 170.751402 0 0 1 854.013267 1023.998208H171.263657A170.495403 170.495403 0 0 1 0.000256 853.246806V170.753194A170.495403 170.495403 0 0 1 171.263657 0.001792zM363.006985 835.070869a15.615945 15.615945 0 0 0-15.615945 15.615946v13.823951a15.359946 15.359946 0 0 0 4.863983 11.263961 14.847948 14.847948 0 0 0 11.51996 4.351985l82.68771-3.839987c27.903902 0 51.199821-1.535995 68.095762-1.535995 25.59991 0 70.143754 1.535995 136.959521 4.607984h22.015923a15.615945 15.615945 0 0 0 15.615945-15.615945v-14.079951a15.615945 15.615945 0 0 0-15.615945-15.615945h-2.303992a143.103499 143.103499 0 0 1-45.82384-5.63198 42.495851 42.495851 0 0 1-24.063916-18.431936 127.999552 127.999552 0 0 1-9.727966-40.191859C588.798195 752.639158 588.798195 721.407267 588.798195 676.351425v-95.487666c0-46.591837 0-108.031622 2.559991-329.214848a15.615945 15.615945 0 0 1 15.615946-15.615945h74.23974c51.199821 0 87.039695 7.167975 104.703633 21.759924a153.599462 153.599462 0 0 1 31.48789 70.399753 15.871944 15.871944 0 0 0 17.663938 11.263961l16.895941-2.559991a15.615945 15.615945 0 0 0 13.055954-17.407939 1800.953697 1800.953697 0 0 1-7.935972-75.007738 981.500565 981.500565 0 0 1-3.327988-82.431711 12.543956 12.543956 0 0 0-4.863983-8.447971 12.287957 12.287957 0 0 0-10.495963-2.559991 236.799171 236.799171 0 0 1-39.167863 6.143979c-25.59991 2.047993-68.351761 2.81599-131.071542 2.81599h-307.198924c-55.807805 0-95.487666 0-119.039584-2.81599a278.527025 278.527025 0 0 1-36.863871-5.375981 15.103947 15.103947 0 0 0-12.799955 2.81599 16.639942 16.639942 0 0 0-6.143978 11.519959c-2.047993 31.231891-4.351985 55.551806-6.655977 72.703746s-7.423974 45.311841-14.847948 81.407715a15.871944 15.871944 0 0 0 14.591949 17.663938l18.687934 3.839987a15.615945 15.615945 0 0 0 18.175937-10.495963 161.535435 161.535435 0 0 1 35.327876-72.703746c19.711931-15.103947 56.319803-22.527921 109.823616-22.527921h71.935748a15.871944 15.871944 0 0 1 11.007961 4.607984 15.359946 15.359946 0 0 1 4.607984 11.007961v276.223033c0 99.327652 0 167.423414-2.047993 204.799284a291.838979 291.838979 0 0 1-7.167974 69.375757 45.311841 45.311841 0 0 1-23.295919 25.59991 126.463557 126.463557 0 0 1-51.199821 7.423974z m0 0"
                  p-id="15984"/>
            </svg>
            <span style="margin-left: 5px; color: #666666">{{ (item.page_content || item).length }}</span>
            </div>
          </div>
          <div class="columnAS" style="width: 100%; font-size: 14px!important; margin-bottom: 10px">
            <div class="rowBC" style="width: 100%">
              <div>
                {{ item.page_content || item }}
              </div>
              <div style="cursor: pointer; font-size: 18px; margin-left: 6px"
                   @click="onHandleDetailContentClick(index)">
                <el-icon v-if="showDetailIndex === index">
                  <ArrowUpBold/>
                </el-icon>
                <el-icon v-else>
                  <ArrowDownBold/>
                </el-icon>
              </div>
            </div>
            <div v-if="showDetailIndex === index" class="detail-content">
              <span style="margin-bottom: 10px">检索文档对应的知识: </span><br/>
              {{
                (item.metadata?.llm_content || item.page_content) || item
              }}
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
// 获取store和router
import {Marked} from "marked";
import {markedHighlight} from "marked-highlight";
import "highlight.js/styles/gruvbox-dark.css";
import hljs from 'highlight.js';
import {ref} from "vue";

const showDetailIndex = ref(-1)

const marked = new Marked(
    markedHighlight({
      langPrefix: 'hljs language-',
      highlight(code, lang, info) {
        const language = hljs.getLanguage(lang) ? lang : 'plaintext';
        return hljs.highlight(code, {language}).value;
      }
    })
);

const props = defineProps({
  message: {required: true, type: Object, default: null},
  isLast: {required: true, type: Boolean, default: false}
})

const isUser = computed(() => props.message.role === 'user')

const roleClass = computed(() => props.message.role === 'user' ? 'right' : 'left')

const emit = defineEmits(['ignore-message-cache'])

const htmlContent = computed(() => {
  return marked.parse(props.message.content)
})

const currentQuoteItem = ref({})

const quoteDialogVisible = ref(false)

const onQuoteClick = (item: object) => {
  currentQuoteItem.value = item
  quoteDialogVisible.value = true
}

const onIgnoreMessageCacheClick = () => {
  emit('ignore-message-cache', props.message)
}

const onHandleDetailContentClick = (index) => {
  if (showDetailIndex.value === index) {
    showDetailIndex.value = -1
  } else {
    showDetailIndex.value = index
  }
}

const navigateTo = (url: string) => {
  window.open(url, '_blank');
}

</script>

<style>
.hljs {
  border-radius: 8px !important;
  padding: 10px !important;
}

.quote-dialog .el-dialog__body {
  padding: 0!important;
}
</style>

<style lang="scss">

.detail-content {
  white-space: pre-wrap;
  border: 1px solid var(--el-color-primary);
  padding: 2px 10px 10px 10px;
  border-radius: 4px;
  color: var(--el-color-primary);
  margin-top: 10px;
  text-align: left;
  width: 100%;
}

.chat-item-container {
  margin: 5px 0;
  display: flex;
  flex-direction: column;
}

.face {
  width: 36px;
  height: 36px;
  border-radius: 36px;
}

.content {
  color: #333333;
  font-size: 14px;
  min-height: 20px;
  border-radius: 10px;
  padding: 0 15px;
  line-height: 1.4;
  word-break: break-all;
  word-wrap: break-word;
  position: relative;
  margin-top: 5px;
  box-shadow: 0 0 5px 5px rgba(0, 0, 0, 0.06);

  .quote-item {
    padding: 5px 10px 5px 0;
    border-radius: 10px;
    border: 1px solid #eeeeee;
    margin-bottom: 6px;
    cursor: pointer;
  }
}

.left {
  margin: 0 10px;

  .face {
  }

  .content {
    color: #333333;
    border: 1px solid #eeeeee;
    border-radius: 0 10px 10px 10px;
  }
}

.right {
  margin: 0 10px;
  flex-direction: row-reverse;

  .face {
  }

  .content {
    color: #41b584;
    background-color: #ecf8f3;
    border: 1px solid #41b584;
    border-radius: 10px 0 10px 10px;
  }
}

.quote-dialog-header {
  cursor: pointer;
  color: #333333;
  text-decoration: underline;
}

.quote-dialog-content-item {
  padding: 10px;
  border: 1px solid #eeeeee;
  border-radius: 10px;
  margin-bottom: 10px;
  width: 100%;
}

</style>

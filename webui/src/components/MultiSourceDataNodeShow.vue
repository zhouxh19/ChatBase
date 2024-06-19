<template>
  <div style="width: 100%">
    <div class="columnSS" style="width: 100%">
      <div style="min-width: 30vw; padding-bottom: 10px; width: 100%">
        <div>
          <el-divider content-position="left">
            <div class="rowSC">
              <el-icon size="18" style="margin-right: 5px"  color="var(--el-color-success)" ><Printer /></el-icon>
              文件名
            </div>
          </el-divider>
          <span style="line-height: 20px; color: #333333">{{ message.file_name }}</span>
        </div>
        <div style="width: 100%">
          <el-divider content-position="left">
            <div class="rowSC">
              <el-icon size="18" style="margin-right: 5px" color="var(--el-color-success)" ><Coin /></el-icon>
              文件内容（仅前6行）
            </div>
          </el-divider>
          <el-table v-if="tableData.length > 0" :data="tableData" style="width: 100%;" height="400" border>
            <el-table-column
                v-for="(item, index) in columnNames"
                :key="index"
                :prop="item"
                :label="item"/>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 获取store和router

const props = defineProps({
  message: {required:true, type: Object, default: null }
})

const columnNames = computed(() => {
  return props.message.header || []
})

const tableData = computed(() => {
  const result: any = [];
  for (let row of props.message.rows) {
    const rowData: any = {};
    for (let i = 0; i < props.message.header.length; i++) {
      rowData[props.message.header[i]] = row[i];
    }
    result.push(rowData);
  }
  return result;
})

</script>

<style>
.el-divider__text {
  background-color: RGBA(251, 251, 252, 1.00);
}
</style>

<style lang="scss">

.chat-item-container {
  margin: 5px 0;
  display: flex;
  flex-direction: column;
}



</style>

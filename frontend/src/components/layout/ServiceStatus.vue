<template>
  <div class="service-status">
    <div style="display: flex; gap: 10px; align-items: center;">
      <el-tag :type="getStatusType(mainStatus)">
        主服务: {{ mainStatus }}
      </el-tag>
      <el-tag :type="getStatusType(pythonStatus)">
        Python: {{ pythonStatus }}
      </el-tag>
      <el-tag :type="getStatusType(rStatus)">
        R: {{ rStatus }}
      </el-tag>
      
      <el-tooltip v-if="lastChecked" :content="`最后检查: ${formatTime(lastChecked)}`">
        <el-button :icon="Refresh" circle size="small" @click="checkServices" :loading="loading" />
      </el-tooltip>
      
      <el-badge v-if="hasUnhealthyServices" is-dot type="danger" class="status-badge">
        <el-icon :size="16" style="cursor: pointer;" @click="showDetails">
          <Warning />
        </el-icon>
      </el-badge>
    </div>
  </div>
</template>

<script setup>
import { Refresh, Warning } from '@element-plus/icons-vue'
import { useHealthStore } from '@/stores/health'
import { storeToRefs } from 'pinia'
import { formatTime } from '@/utils/helpers'
import { ElMessage } from 'element-plus'

const healthStore = useHealthStore()
const { checkServices } = healthStore
const { 
  mainStatus, 
  pythonStatus, 
  rStatus, 
  loading, 
  lastChecked,
  allServicesHealthy,
  hasUnhealthyServices,
  formattedLastChecked 
} = storeToRefs(healthStore)

const getStatusType = (status) => {
  if (status === '正常') return 'success'
  if (status === '未启动') return 'warning'
  if (status === '异常') return 'danger'
  return 'info'
}

const showDetails = () => {
  if (hasUnhealthyServices.value) {
    ElMessage.warning({
      message: `服务状态: 主服务(${mainStatus.value}), Python(${pythonStatus.value}), R(${rStatus.value})`,
      duration: 5000
    })
  }
}
</script>

<style scoped>
.service-status {
  display: flex;
  align-items: center;
}

.status-badge {
  margin-left: 5px;
  cursor: pointer;
}
</style>
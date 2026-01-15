<template>
  <div class="dataset-list">
    <el-card class="dataset-card">
      <template #header>
        <div class="card-header">
          <h3>我的数据集</h3>
          <el-button type="primary" @click="$router.push('/datasets/upload')">
            <el-icon><Upload /></el-icon>
            上传数据集
          </el-button>
        </div>
      </template>
      
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索数据集"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
          style="width: 300px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <div class="filter-actions">
          <el-select v-model="filterType" placeholder="文件类型" clearable>
            <el-option label="CSV" value="csv" />
            <el-option label="Excel" value="excel" />
            <el-option label="JSON" value="json" />
          </el-select>
          
          <el-select v-model="sortField" placeholder="排序方式">
            <el-option label="创建时间" value="created_at" />
            <el-option label="文件大小" value="file_size" />
            <el-option label="名称" value="name" />
          </el-select>
        </div>
      </div>
      
      <el-table
        :data="datasets"
        v-loading="loading"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="name" label="名称" sortable="custom">
          <template #default="{ row }">
            <router-link :to="`/datasets/${row.id}`" class="dataset-name">
              {{ row.name }}
            </router-link>
          </template>
        </el-table-column>
        
        <el-table-column prop="row_count" label="行数" width="100">
          <template #default="{ row }">
            {{ formatNumber(row.row_count) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="columns.length" label="列数" width="100" />
        
        <el-table-column prop="file_size" label="大小" width="120" sortable="custom">
          <template #default="{ row }">
            {{ formatFileSize(row.file_size) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="file_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getFileTypeTag(row.file_type)">
              {{ row.file_type.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="is_public" label="可见性" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_public ? 'success' : 'info'">
              {{ row.is_public ? '公开' : '私有' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="180" sortable="custom">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handlePreview(row)">
              预览
            </el-button>
            <el-dropdown @command="handleActionCommand(row, $event)">
              <el-button size="small">
                更多<el-icon><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="analyze">分析</el-dropdown-item>
                  <el-dropdown-item command="download">下载</el-dropdown-item>
                  <el-dropdown-item command="share" v-if="!row.is_public">
                    设为公开
                  </el-dropdown-item>
                  <el-dropdown-item command="delete" divided>
                    <span style="color: var(--danger-color)">删除</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Upload, ArrowDown } from '@element-plus/icons-vue'
import { useDatasetStore } from '@/stores/dataset'
import type { Dataset } from '@/types'
import { formatDate, formatFileSize, formatNumber } from '@/utils/format'

const router = useRouter()
const datasetStore = useDatasetStore()

const searchQuery = ref('')
const filterType = ref('')
const sortField = ref('created_at')
const sortOrder = ref('desc')
const currentPage = ref(1)
const pageSize = ref(10)

const loading = ref(false)

const datasets = computed(() => datasetStore.datasets)
const total = computed(() => datasetStore.total)

const fetchDatasets = async () => {
  loading.value = true
  try {
    await datasetStore.fetchDatasets({
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchQuery.value,
      file_type: filterType.value,
      sort_field: sortField.value,
      sort_order: sortOrder.value
    })
  } catch (error) {
    ElMessage.error('获取数据集失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchDatasets()
}

const handleSortChange = ({ prop, order }: any) => {
  sortField.value = prop
  sortOrder.value = order === 'ascending' ? 'asc' : 'desc'
  fetchDatasets()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchDatasets()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  fetchDatasets()
}

const getFileTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    csv: 'success',
    excel: 'warning',
    json: 'info'
  }
  return typeMap[type] || 'default'
}

const handlePreview = (dataset: Dataset) => {
  router.push(`/datasets/${dataset.id}`)
}

const handleActionCommand = async (dataset: Dataset, command: string) => {
  switch (command) {
    case 'analyze':
      router.push({
        path: '/analysis',
        query: { dataset_id: dataset.id }
      })
      break
      
    case 'download':
      try {
        await datasetStore.downloadDataset(dataset.id)
        ElMessage.success('下载任务已开始')
      } catch (error) {
        ElMessage.error('下载失败')
      }
      break
      
    case 'share':
      try {
        await datasetStore.updateDatasetVisibility(dataset.id, true)
        ElMessage.success('数据集已设为公开')
        fetchDatasets()
      } catch (error) {
        ElMessage.error('操作失败')
      }
      break
      
    case 'delete':
      try {
        await ElMessageBox.confirm(
          `确认删除数据集 "${dataset.name}"？`,
          '确认删除',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        await datasetStore.deleteDataset(dataset.id)
        ElMessage.success('删除成功')
        fetchDatasets()
      } catch (error) {
        // 用户取消删除
      }
      break
  }
}

onMounted(() => {
  fetchDatasets()
})
</script>

<style lang="scss" scoped>
.dataset-list {
  .dataset-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .search-bar {
      display: flex;
      justify-content: space-between;
      margin-bottom: 20px;
      
      .filter-actions {
        display: flex;
        gap: 10px;
        
        .el-select {
          width: 120px;
        }
      }
    }
    
    .dataset-name {
      color: var(--primary-color);
      text-decoration: none;
      
      &:hover {
        text-decoration: underline;
      }
    }
    
    .pagination {
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }
}
</style>
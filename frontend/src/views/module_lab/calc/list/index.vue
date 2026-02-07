<!-- 功能 -->
<template>
  <div class="app-container">
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <div class="card-header__main">
            <!-- 左侧：标题 -->
            <span class="card-header__title">功能列表</span>
            
            <!-- 右侧：控制按钮 -->
            <div class="card-header__controls">
              <el-button-group>
                <el-tooltip content="显示/隐藏搜索功能" placement="top">
                  <el-button 
                    size="small" 
                    type="primary" 
                    :plain="!showSearch" 
                    @click="toggleSearch"
                  >
                    <el-icon><Search /></el-icon>
                    搜索
                  </el-button>
                </el-tooltip>
                <el-tooltip content="显示/隐藏排序功能" placement="top">
                  <el-button 
                    size="small" 
                    type="success" 
                    :plain="!showSort" 
                    @click="toggleSort"
                  >
                    <el-icon><Sort /></el-icon>
                    排序
                  </el-button>
                </el-tooltip>
              </el-button-group>
              
              <!-- 排序控件（可收起） -->
              <div v-if="showSort" class="card-header__sort">
                <el-select v-model="sortField" placeholder="选择排序字段" size="small" style="width: 120px; margin-right: 8px;"
                  @change="handleSortChange">
                  <el-option label="功能名称" value="name" />
                  <el-option label="研究领域" value="field" />
                  <el-option label="功能类别" value="category" />
                </el-select>

                <el-select v-model="sortOrder" placeholder="选择排序顺序" size="small" style="width: 100px; margin-right: 8px;"
                  @change="handleSortChange">
                  <el-option label="升序" value="asc" />
                  <el-option label="降序" value="desc" />
                </el-select>

                <el-button type="text" size="small" @click="resetSort" v-if="sortField !== 'field' || sortOrder !== 'desc'">
                  重置默认
                </el-button>
              </div>
            </div>
          </div>
          
          <!-- 搜索区域（可收起） -->
          <transition name="el-fade-in">
            <div v-if="showSearch" class="card-header__search">
              <el-form ref="queryFormRef" :model="queryFormData" label-suffix=":" :inline="true"
                @submit.prevent="handleQuery">
                <el-form-item label="功能名称" prop="name">
                  <el-input v-model="queryFormData.name" placeholder="请输入功能名称" clearable size="small" />
                </el-form-item>
                <el-form-item label="研究领域" prop="field">
                  <el-input v-model="queryFormData.field" placeholder="请输入研究领域" clearable size="small" />
                </el-form-item>
                <el-form-item label="功能类别" prop="category">
                  <el-input v-model="queryFormData.category" placeholder="请输入功能类别" clearable size="small" />
                </el-form-item>
                <el-form-item label="备注/描述" prop="description">
                  <el-input v-model="queryFormData.description" placeholder="请输入备注/描述" clearable size="small" />
                </el-form-item>

                <!-- 查询按钮 -->
                <el-form-item>
                  <el-button v-hasPerm="['module_lab:calc:query']" type="primary" icon="search" size="small" @click="handleQuery">
                    查询
                  </el-button>
                  <el-button size="small" @click="resetQuery">
                    重置
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </transition>
        </div>
      </template>

      <!-- 卡片列表区域 -->
      <div v-loading="loading" class="card-list-container">
        <template v-if="sortedPageTableData.length > 0">
          <div class="card-list">
            <div v-for="item in sortedPageTableData" :key="item.id" class="card-item" @click="handleOpenDetail(item)">
              <div class="card-image-container">
                <el-image v-if="item.image" :src="item.image" fit="cover" lazy class="card-image"
                  :preview-src-list="[item.image]" :preview-teleported="true" @click.stop />
                <div v-else class="card-image-placeholder">
                  <el-icon class="placeholder-icon">
                    <Picture />
                  </el-icon>
                  <span>暂无图片</span>
                </div>
              </div>
              <div class="card-info">
                <h3 class="card-title">{{ item.name }}</h3>
                <div class="card-tags">
                  <el-tag v-if="item.field" size="small" type="primary">{{ item.field }}</el-tag>
                </div>
              </div>
              <!-- 悬停时显示描述 -->
              <div class="card-hover-overlay">
                <div class="overlay-content">
                  <div class="overlay-description">
                    <h3 style="color: gold;">{{ item.category }}</h3>
                    <p>{{ item.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
        <template v-else>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
      </div>

      <!-- 分页区域 -->
      <template #footer>
        <pagination v-model:total="total" v-model:page="queryFormData.page_no" v-model:limit="queryFormData.page_size"
          @pagination="loadingData" />
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "LabCalcList",
  inheritAttrs: false,
});

import { ref, reactive, onMounted, computed, onUnmounted } from "vue";
import { Picture, Search, Sort } from "@element-plus/icons-vue";
import { useDictStore } from "@/store";
import { useRouter } from 'vue-router'

import LabCalcAPI, {
  LabCalcPageQuery,
  LabCalcTable,
} from "@/api/module_lab/calc";

const queryFormRef = ref();
const total = ref(0);
const loading = ref(false);

// 控制显示/隐藏
const showSearch = ref(true);
const showSort = ref(true);
const isMobile = ref(false);

// 排序相关
const sortField = ref('field'); // 默认排序字段：研究领域
const sortOrder = ref('desc');  // 默认排序顺序：降序

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore();
const dictTypes: any = [];

// 分页表单
const pageTableData = ref<LabCalcTable[]>([]);

// 计算排序后的数据
const sortedPageTableData = computed(() => {
  if (!pageTableData.value.length) return [];

  return [...pageTableData.value].sort((a, b) => {
    const aValue = a[sortField.value as keyof typeof a];
    const bValue = b[sortField.value as keyof typeof b];

    if (aValue === null || aValue === undefined) return 1;
    if (bValue === null || bValue === undefined) return -1;

    // 根据排序顺序进行比较
    let result = 0;

    if (typeof aValue === 'string' && typeof bValue === 'string') {
      // 字符串比较（中文按拼音首字母）
      result = aValue.localeCompare(bValue, 'zh-CN');
    } else if (typeof aValue === 'number' && typeof bValue === 'number') {
      // 数字比较
      result = aValue - bValue;
    } else if (aValue instanceof Date && bValue instanceof Date) {
      // 日期比较
      result = aValue.getTime() - bValue.getTime();
    } else {
      // 其他类型转为字符串比较
      result = String(aValue).localeCompare(String(bValue), 'zh-CN');
    }

    // 根据排序顺序调整结果
    return sortOrder.value === 'desc' ? -result : result;
  });
});

// 分页查询参数
const queryFormData = reactive<LabCalcPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  field: undefined,
  category: undefined,
  description: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 切换搜索显示
const toggleSearch = () => {
  showSearch.value = !showSearch.value;
};

// 切换排序显示
const toggleSort = () => {
  showSort.value = !showSort.value;
};

// 排序改变处理
const handleSortChange = () => {
  console.log(`排序字段: ${sortField.value}, 排序顺序: ${sortOrder.value}`);
};

// 重置排序
const resetSort = () => {
  sortField.value = 'field';
  sortOrder.value = 'desc';
};

// 重置查询条件
const resetQuery = () => {
  if (queryFormRef.value) {
    queryFormRef.value.resetFields();
    queryFormData.page_no = 1;
    loadingData();
  }
};

// 检测屏幕大小
const checkScreenSize = () => {
  isMobile.value = window.innerWidth < 768;
  // 在小屏幕上默认收起搜索和排序
  if (isMobile.value && showSearch.value && showSort.value) {
    showSearch.value = false;
    showSort.value = false;
  }
};

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await LabCalcAPI.listLabCalc(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

const router = useRouter()

const handleOpenDetail = (row: any) => {
  const routeData = router.resolve({
    path: '/lab/calc/detail',
    query: { id: row.id }
  });
  const url = window.location.origin + routeData.href;
  window.open(url, '_blank');
};

// 页面挂载时检测屏幕大小
onMounted(async () => {
  // 预加载字典数据
  if (dictTypes.length > 0) {
    await dictStore.getDict(dictTypes);
  }
  
  checkScreenSize();
  window.addEventListener('resize', checkScreenSize);
  
  loadingData();
});

// 页面卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('resize', checkScreenSize);
});
</script>

<style lang="scss" scoped>
.app-container {
  .data-table {
    margin: 20px;
  }
  
  .card-header {
    padding-bottom: 0;
    
    &__main {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 16px;
    }
    
    &__title {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
      flex-shrink: 0;
    }
    
    &__controls {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      
      .el-button-group {
        flex-shrink: 0;
        
        .el-button {
          .el-icon {
            margin-right: 4px;
          }
        }
      }
    }
    
    &__sort {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      background: #f8f9fa;
      padding: 8px 12px;
      border-radius: 4px;
      border: 1px solid #ebeef5;
      
      .el-select {
        flex-shrink: 0;
        
        :deep(.el-input__inner) {
          font-size: 12px;
        }
      }
      
      .el-button {
        color: #909399;
        flex-shrink: 0;
        
        &:hover {
          color: #409eff;
        }
      }
    }
    
    &__search {
      border-top: 1px solid #e4e7ed;
      padding-top: 16px;
      padding-bottom: 8px;
      
      .el-form {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        align-items: center;
        
        .el-form-item {
          margin-bottom: 0;
          margin-right: 0;
          flex: 1 1 200px;
          min-width: 180px;
          
          :deep(.el-form-item__label) {
            width: 80px;
            text-align: right;
            padding-right: 8px;
          }
          
          :deep(.el-form-item__content) {
            flex: 1;
            min-width: 120px;
          }
        }
        
        // 按钮组不参与flex分配
        .el-form-item:last-child {
          flex: 0 0 auto;
          min-width: auto;
          margin-left: auto;
        }
      }
    }
  }
  
  .card-list-container {
    min-height: 200px;
  }
  
  .card-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 16px;
    padding: 10px;
  }
  
  .card-item {
    position: relative;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 130px;
    width: 100px;
    display: flex;
    flex-direction: column;
    background: #fff;
    
    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      border-color: #409eff;
      
      .card-hover-overlay {
        opacity: 1;
        visibility: visible;
      }
    }
  }
  
  .card-image-container {
    height: 80px;
    width: 100%;
    overflow: hidden;
    background: #f5f7fa;
    
    .card-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }
    
    .card-image-placeholder {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #909399;
      
      .placeholder-icon {
        font-size: 24px;
        margin-bottom: 4px;
        opacity: 0.5;
      }
      
      span {
        font-size: 10px;
      }
    }
    
    &:hover .card-image {
      transform: scale(1.05);
    }
  }
  
  .card-info {
    padding: 6px;
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .card-title {
    margin: 0;
    font-size: 12px;
    font-weight: 500;
    color: #303133;
    line-height: 1.3;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .card-tags {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-top: 4px;
    align-items: center;
    
    .el-tag {
      height: 16px;
      line-height: 14px;
      font-size: 10px;
      padding: 0 4px;
      border-radius: 2px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 90px;
    }
  }
  
  .card-hover-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(64, 158, 255, 0.95);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    visibility: hidden;
    transition: all 0.2s ease;
    padding: 8px;
    text-align: center;
    
    .overlay-content {
      width: 100%;
      max-height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    
    .overlay-description {
      font-size: 11px;
      line-height: 1.4;
      max-height: 80px;
      overflow: auto;
      word-break: break-word;
      margin-bottom: 6px;
    }
    
    .overlay-action {
      font-size: 10px;
      opacity: 0.9;
      border: 1px solid rgba(255, 255, 255, 0.5);
      border-radius: 2px;
      padding: 2px 4px;
      display: inline-block;
    }
  }
  
  // 响应式调整
  @media (max-width: 1200px) {
    .card-header__search .el-form .el-form-item {
      flex: 1 1 180px;
      min-width: 160px;
    }
  }
  
  @media (max-width: 992px) {
    .card-header__search .el-form .el-form-item {
      flex: 1 1 160px;
      min-width: 140px;
    }
  }
  
  @media (max-width: 768px) {
    .card-header {
      &__main {
        flex-direction: column;
        align-items: stretch;
        gap: 12px;
      }
      
      &__controls {
        justify-content: space-between;
      }
      
      &__sort {
        width: 100%;
        justify-content: center;
        flex-direction: column;
        align-items: stretch;
        
        .el-select {
          width: 100%;
          margin-bottom: 8px;
          margin-right: 0;
        }
        
        .el-button {
          align-self: center;
        }
      }
    }
    
    .card-list {
      grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
      gap: 12px;
    }
    
    .card-header__search .el-form {
      flex-direction: column;
      align-items: stretch;
      
      .el-form-item {
        width: 100%;
        flex: 1 1 auto;
        min-width: auto;
        
        :deep(.el-form-item__label) {
          width: 80px;
          text-align: right;
        }
        
        :deep(.el-form-item__content) {
          width: calc(100% - 80px);
        }
      }
      
      .el-form-item:last-child {
        width: 100%;
        margin-left: 0;
        display: flex;
        justify-content: center;
        gap: 10px;
      }
    }
  }
  
  @media (max-width: 576px) {
    .card-list {
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
    }
    
    .card-header__sort {
      padding: 6px;
      
      .el-select {
        margin-bottom: 6px;
      }
    }
    
    .card-header__search {
      padding-top: 12px;
      
      .el-form .el-form-item {
        :deep(.el-form-item__label) {
          width: 70px;
          font-size: 12px;
        }
      }
    }
    
    .card-item {
      width: auto;
      max-width: 100px;
    }
  }
  
  @media (max-width: 400px) {
    .card-list {
      grid-template-columns: repeat(2, 1fr);
    }
    
    .card-header__controls {
      flex-direction: column;
      align-items: stretch;
      gap: 8px;
    }
  }
}
</style>